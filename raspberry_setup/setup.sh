#!/bin/bash
if [[ "$EUID" != 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi

if [[ "$PWD" != /home/pi/indi-lite-tools/raspberry_setup ]]; then
    echo "This scripts need to be installed and executed from indi-lite-tools"
    exit 1
fi

PYTHON_VERSION=2
ASSUME_YES=false

while [[ -n "$1" ]]; do

    case "$1" in
        --yes|-y)
            ASSUME_YES=true
            ;;
        --python3|-3)
            PYTHON_VERSION=3
            ;;
        *)
            echo "Usage: $0 options"
            echo "Options:"
            echo "-y|--yes      Assume yes to all questions"
            echo "-3|--python3  Use python3 instead of python2"
            exit 1
            ;;
    esac
    shift
done
full_upgrade() {
	apt-get update && apt-get dist-upgrade -y
}

python_pkgname=python
[[ "$PYTHON_VERSION" == 3 ]] && python_pkgname=python3

install_prerequisites() {
    apt-get update && apt-get install -y cdbs libcfitsio3-dev libnova-dev libusb-1.0-0-dev libjpeg-dev \
        libusb-dev libtiff5-dev libftdi-dev fxload libkrb5-dev libcurl4-gnutls-dev libraw-dev libgphoto2-dev \
        libgsl0-dev dkms libboost-regex-dev libgps-dev libdc1394-22-dev vim curl wget nginx \
        ${python_pkgname}-pip i${python_pkgname} ${python_pkgname}-dev git hostapd tmux dnsmasq swig shellinabox libfreetype6-dev fonts-dejavu-core 
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

enable_hwclock() {
    sed -i 's/dtparam=i2c_arm=.*//g' /boot/config.txt
    echo dtparam=i2c_arm=on >> /boot/config.txt
    sed -i 's/dtoverlay=i2c-rtc.*//g' /boot/config.txt
    read -e -i "ds3231" -p "Enter RTC module to be used: " rtc_module
    echo "dtoverlay=i2c-rtc,$rtc_module" >> /boot/config.txt
    apt-get purge -y fake-hwclock
    grep -q i2c-dev /etc/modules || echo 'i2c-dev' >> /etc/modules
    cp hwclock/hwclock.service /etc/systemd/system/
    systemctl enable hwclock && systemctl start hwclock 
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
    cp -av home-settings/python_modules home-settings/bin ~pi
    chown -R pi:pi ~pi/bin
    chown -R pi:pi ~pi/python_modules
}

setup_python() {
    pip${PYTHON_VERSION} install -U pip setuptools
    pip${PYTHON_VERSION}  install flask pyindi-client requests psutil bottle max7219 luma.led_matrix luma.oled astropy
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
    [[ -r /etc/hostapd/.wifi_setup ]] && . /etc/hostapd/.wifi_setup
    read -p "Enter your wifi access point ESSID: " -e AP_ESSID -i "$AP_ESSID"
    read -p "Enter your wifi access point secret: " -e AP_SECRET -i "$AP_SECRET"
    cp wifi-ap/ap-mode /usr/local/bin/
    cp wifi-ap/dhcpcd.conf-ap-* wifi-ap/dnsmasq.conf /etc/
    cp wifi-ap/interfaces-ap-* /etc/network/
    cp wifi-ap/hostapd.conf /etc/hostapd/
    cp wifi-ap/hostapd /etc/default/
    [[ -n "$AP_ESSID" ]] && sed -i "s^___WPA_PASSPHRASE___^$AP_SECRET^g" /etc/hostapd/hostapd.conf
    [[ -n "$AP_SECRET" ]] && sed -i "s^___ESSID___^$AP_ESSID^g" /etc/hostapd/hostapd.conf
    cat >/etc/hostapd/.wifi_setup <<EOF
export AP_SECRET="$AP_SECRET"
export AP_ESSID="$AP_ESSID"
EOF
    echo "To activate and deactivate wifi access point (only for wlan0), just run ap-mode enable/disable"
}

setup_dashboard() {
    cp ../dashboard/indi-dashboard.service /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable indi-dashboard
    systemctl start indi-dashboard
}

setup_hdmi() {
    cp hdmi-control/hdmi-control /usr/bin
    cp hdmi-control/hdmi-control.service /etc/systemd/system
    read -e -n 1 -p "Disable HDMI port on system startup? (saves a few mA of current) [Y/n] " disable_hdmi
    [ "$disable_hdmi" == n ] && HDMI_ENABLED=1 || HDMI_ENABLED=0
    echo "export HDMI_ENABLED=$HDMI_ENABLED" > /etc/hdmi-control.conf
    systemctl daemon-reload
    systemctl enable hdmi-control
    systemctl restart hdmi-control
}


setup_shellinabox() {
    cp shellinabox/shellinabox /etc/default
    cp shellinabox/indi-tmux /usr/local/bin
    systemctl enable shellinabox
    systemctl start shellinabox
    rm -f "/etc/shellinabox/options-enabled/01_Monochrome.css"
    rm -f "/etc/shellinabox/options-enabled/00+Black on White.css"
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

ask_step "Upgrade packages?" full_upgrade
ask_step "Enable ssh on boot?" enable_ssh
ask_step "Install dependencies?" install_prerequisites
ask_step "Install latest INDI?" install_indi
ask_step "Enable SPI interface?" enable_spi
ask_step "Enable GPIO/I2C hwclock support?" enable_hwclock
ask_step "Disable audio?" disable_audio
ask_step "Setup home directory layout/bashrc?" setup_home
ask_step "Setup nginx?" setup_nginx
ask_step "Setup wifi access point?" setup_wifi_ap
ask_step "Setup python modules?" setup_python
ask_step "Setup Adafruit DHT modules?" setup_AdafruitDHT
ask_step "Setup INDI Dashboard?" setup_dashboard
ask_step "Setup HDMI control?" setup_hdmi
ask_step "Setup Shellinabox?" setup_shellinabox
ask_step "Setup INDI Control Panel?" setup_indi_control_panel

