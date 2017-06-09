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
    apt-get update && apt-get install -y cdbs libcfitsio3-dev libnova-dev libusb-1.0-0-dev libjpeg-dev libusb-dev libtiff5-dev libftdi-dev fxload libkrb5-dev libcurl4-gnutls-dev libraw-dev libgphoto2-dev libgsl0-dev dkms libboost-regex-dev libgps-dev libdc1394-22-dev vim curl wget nginx python3-virtualenv python3-pip ipython3 git hostapd tmux dnsmasq
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

setup_home() {
    bashrc_local_file="$(readlink -f home-settings/bashrc)"
    sudo -u pi bash <<EOF
    cd /home/pi
    mkdir -p bin python_modules
    grep "$bashrc_local_file" .bashrc -q || echo "source \"$bashrc_local_file\"" >> .bashrc
EOF
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


ask_step() {
    read -p "$1 [Y/n]" -n 1 -e confirm
    shift
    if [[ "$confirm" == "n" ]]; then
        return
    fi
    "$@"
}

ask_step "Install dependencies?" install_prerequisites
ask_step "Install latest INDI?" install_indi
ask_step "Enable SPI interface?" enable_spi
ask_step "Disable audio?" disable_audio
ask_step "Setup home directory layout/bashrc?" setup_home
ask_step "Setup nginx?" setup_nginx
ask_step "Setup wifi access point?" setup_wifi_ap
