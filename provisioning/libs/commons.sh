
setup_shell() {
    cp -av "$SCRIPT_PATH/shell-env/bashrc" /etc/profile.d/indi-lite-tools.sh
}

setup_python() {
    pip${PYTHON_VERSION} install -U pip setuptools
    pip${PYTHON_VERSION}  install flask requests psutil bottle luma.led_matrix luma.oled astropy
    CFLAGS="-std=c++11" pip${PYTHON_VERSION} install pyindi-client 
}

setup_nginx() {
    rm /etc/nginx/sites-enabled/*
    cp -av "$SCRIPT_PATH"/nginx/indi_proxy /etc/nginx/sites-available
    ln -s /etc/nginx/sites-available/indi_proxy /etc/nginx/sites-enabled/
    cp -av "$SCRIPT_PATH"/nginx/ssl/ /etc/nginx/
    systemctl enable nginx
    systemctl restart nginx
}

setup_wifi_ap() {
    [[ -z "$AP_ESSID" ]] && AP_ESSID="$HOSTNAME"
    [[ -r /etc/hostapd/.wifi_setup ]] && . /etc/hostapd/.wifi_setup
    read -p "Enter your wifi access point ESSID: " -i "$AP_ESSID" -e AP_ESSID
    read -p "Enter your wifi access point secret: " -i "$AP_SECRET" -e AP_SECRET
    cp "$SCRIPT_PATH/"wifi-ap/ap-mode /usr/local/bin/
    cp "$SCRIPT_PATH/"wifi-ap/dhcpcd.conf-ap-* "$SCRIPT_PATH/"wifi-ap/dnsmasq.conf /etc/
    cp "$SCRIPT_PATH/"wifi-ap/interfaces-ap-* /etc/network/
    cp "$SCRIPT_PATH/"wifi-ap/hostapd.conf /etc/hostapd/
    cp "$SCRIPT_PATH/"wifi-ap/hostapd /etc/default/
    [[ -n "$AP_ESSID" ]] && sed -i "s^___WPA_PASSPHRASE___^$AP_SECRET^g" /etc/hostapd/hostapd.conf
    [[ -n "$AP_SECRET" ]] && sed -i "s^___ESSID___^$AP_ESSID^g" /etc/hostapd/hostapd.conf
    cat >/etc/hostapd/.wifi_setup <<EOF
export AP_SECRET="$AP_SECRET"
export AP_ESSID="$AP_ESSID"
EOF
    echo "To activate and deactivate wifi access point (only for wlan0), just run ap-mode enable/disable"
}

setup_dashboard() {
    sed "s/%%%USER%%%/$indi_user/g" "$PROJECT_PATH"/dashboard/indi-dashboard.service > /etc/systemd/system/indi-dashboard.service
    systemctl daemon-reload
    systemctl enable indi-dashboard
    systemctl start indi-dashboard
}


setup_shellinabox() {
    cp "$SCRIPT_PATH/"shellinabox/shellinabox /etc/default
    cp "$SCRIPT_PATH/"shellinabox/indi-tmux /usr/local/bin
    systemctl enable shellinabox
    systemctl start shellinabox
    rm -f "/etc/shellinabox/options-enabled/01_Monochrome.css"
    rm -f "/etc/shellinabox/options-enabled/00+Black on White.css"
    cat >>/etc/default/shellinabox <<EOF
SHELLINABOX_ARGS="--no-beep --disable-ssl --service /:$sh_user:$sh_user:/home/$sh_user:'/usr/local/bin/indi-tmux'"
EOF
}

setup_AdafruitDHT() {
    prevdir="$PWD"
    cd /tmp
    git clone https://github.com/adafruit/Adafruit_Python_DHT.git
    cd Adafruit_Python_DHT
    sudo python${PYTHON_VERSION} setup.py install
    cd "$prevdir"
    rm -rf /tmp/Adafruit_Python_DHT
}

setup_indi_control_panel() {
    pip"${PYTHON_VERSION}" install -U indiweb
    curl https://raw.githubusercontent.com/knro/indiwebmanager/master/indiwebmanager.service | sed "s|User=pi|User=$indi_user|g" > /etc/systemd/system/indiwebmanager.service

    systemctl daemon-reload
    systemctl enable indiwebmanager
    systemctl start indiwebmanager
}

ask_step() {
    if [[ "$ASSUME_YES" == true ]]; then
        confirm=y
    else
        read -p "$1 [Y/n] " -n 1 -e confirm
    fi
    shift
    if [[ "$confirm" == "n" ]]; then
        return
    fi
    "$@"
}

copy_files() {
    rm -rf "$TARGET_DIRECTORY"
    cp -a "$PROJECT_PATH" "$TARGET_DIRECTORY"
}


