#!/bin/bash
if [[ "$EUID" != 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi

if [[ "$PWD" != /home/pi/indi-lite-tools/raspberry_setup ]]; then
    echo "This scripts need to be installed and executed from indi-lite-tools"
    exit 1
fi

install_prerequisites() {
    apt-get update && apt-get install -y cdbs libcfitsio3-dev libnova-dev libusb-1.0-0-dev libjpeg-dev \
        libusb-dev libtiff5-dev libftdi-dev fxload libkrb5-dev libcurl4-gnutls-dev libraw-dev libgphoto2-dev \
        libgsl0-dev dkms libboost-regex-dev libgps-dev libdc1394-22-dev vim curl wget nginx \
        python-pip ipython python-dev git hostapd tmux dnsmasq swig shellinabox
}

install_indi() {
    mkdir /tmp/indi_install
    cd /tmp/indi_install
    wget "indilib.org/jdownloads/Raspberry PI/libindi_1.4.1_rpi.tar.gz"
    tar xf "libindi_1.4.1_rpi.tar.gz"
    dpkg -i libindi*/*.deb
    cd -
    rm -rf /tmp/indi_install
}

enable_spi() {
    sed -i 's/dtparam=spi=.*//g' /boot/config.txt
    echo dtparam=spi=on >> /boot/config.txt
}

disable_audio() {
    sed -i 's/dtparam=audio=on/dtparam=audio=off/g' /boot/config.txt
}

enable_ssh() {
    touch /boot/ssh
}

setup_home() {
    bashrc_local_file="$(readlink -f home-settings/bashrc)"
    sudo -u pi bash <<EOF
    cd /home/pi
    mkdir -p bin python_modules
    grep "$bashrc_local_file" .bashrc -q || echo "source \"$bashrc_local_file\"" >> .bashrc
EOF
    cp home-settings/bin/* ~pi/bin
    chown pi:pi ~pi/bin/*
}

setup_python() {
    pip2 install -U pip setuptools
    pip2 install flask pyindi-client requests psutil bottle max7219 luma.led_matrix
}

setup_nginx() {
    rm /etc/nginx/sites-enabled/*
    cp -av nginx/indi_proxy /etc/nginx/sites-available
    ln -s /etc/nginx/sites-available/indi_proxy /etc/nginx/sites-enabled/
    cp -av nginx/ssl/ /etc/nginx/
    systemctl enable nginx
    systemctl restart nginx
}

setup_wifi_ap() {
    # TODO: read from existing config if found    
    read -p "Enter your wifi access point ESSID: " -e AP_ESSID
    read -p "Enter your wifi access point secret: " -e AP_SECRET
    cp wifi-ap/ap-mode /usr/local/bin/
    cp wifi-ap/dhcpcd.conf-ap-* wifi-ap/dnsmasq.conf /etc/
    cp wifi-ap/interfaces-ap-* /etc/network/
    cp wifi-ap/hostapd.conf /etc/hostapd/
    cp wifi-ap/hostapd /etc/default/
    [[ -n "$AP_ESSID" ]] && sed -i "s^___WPA_PASSPHRASE___^$AP_SECRET^g" /etc/hostapd/hostapd.conf
    [[ -n "$AP_SECRET" ]] && sed -i "s^___ESSID___^$AP_ESSID^g" /etc/hostapd/hostapd.conf
    echo "To activate and deactivate wifi access point (only for wlan0), just run ap-mode enable/disable"
}

setup_control_panel() {
    cp ../control-panel/raspberry-control-panel.service /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable raspberry-control-panel
    systemctl start raspberry-control-panel
}

setup_shellinabox() {
    cp shellinabox/shellinabox /etc/default
    cp shellinabox/indi-tmux /usr/local/bin
    systemctl enable shellinabox
    systemctl start shellinabox
}

setup_AdafruitDHT() {
    prevdir="$PWD"
    cd /tmp
    git clone https://github.com/adafruit/Adafruit_Python_DHT.git
    cd Adafruit_Python_DHT
    sudo python setup.py install
    cd "$prevdir"
    rm -rf /tmp/Adafruit_Python_DHT
}

setup_indi_control_panel() {

    sudo -u pi bash <<EOF
    cd /home/pi
    if [[ -d indiwebmanager ]]; then
        cd indiwebmanager && git pull

    else
        git clone https://github.com/knro/indiwebmanager.git
    fi
EOF
    cp /home/pi/indiwebmanager/indiwebmanager.service /etc/systemd/system
    sed -i 's|/home/pi/servermanager|/home/pi/indiwebmanager/servermanager|g' /etc/systemd/system/indiwebmanager.service

    systemctl daemon-reload
    systemctl enable indiwebmanager
    systemctl start indiwebmanager
}

ask_step() {
read -p "$1 [Y/n] " -n 1 -e confirm
    shift
    if [[ "$confirm" == "n" ]]; then
        return
    fi
    "$@"
}

ask_step "Enable ssh on boot?" enable_ssh
ask_step "Install dependencies?" install_prerequisites
ask_step "Install latest INDI?" install_indi
ask_step "Enable SPI interface?" enable_spi
ask_step "Disable audio?" disable_audio
ask_step "Setup home directory layout/bashrc?" setup_home
ask_step "Setup nginx?" setup_nginx
ask_step "Setup wifi access point?" setup_wifi_ap
ask_step "Setup python modules?" setup_python
ask_step "Setup Adafruit DHT modules?" setup_AdafruitDHT
ask_step "Setup Raspberry control panel?" setup_control_panel
ask_step "Setup Shellinabox?" setup_shellinabox
ask_step "Setup INDI Control Panel?" setup_indi_control_panel

