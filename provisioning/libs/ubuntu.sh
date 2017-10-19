

full_upgrade() {
	apt-get update && apt-get dist-upgrade -y
}

install_prerequisites() {
    apt-get update && apt-get install -y cdbs libcfitsio3-dev libnova-dev libusb-1.0-0-dev libjpeg-dev \
        libusb-dev libtiff5-dev libftdi-dev fxload libkrb5-dev libcurl4-gnutls-dev libraw-dev libgphoto2-dev \
        libgsl0-dev dkms libboost-regex-dev libgps-dev libdc1394-22-dev vim curl wget nginx \
        ${python_pkgname}-pip i${python_pkgname} ${python_pkgname}-dev git hostapd tmux dnsmasq swig shellinabox libfreetype6-dev fonts-dejavu-core 
}

add_indi() {
    add-apt-repository ppa:mutlaqja/ppa
    apt-get update
    apt-get install -y indi-full
}

install_distro_steps() {
    ask_step "Upgrade packages?" full_upgrade
    ask_step "Install dependencies?" install_prerequisites
    ask_step "add INDI ppa and install bleeding edge INDI?" add_indi
    ask_step "Setup shell environment?" setup_shell
    ask_step "Setup nginx?" setup_nginx
    ask_step "Setup wifi access point?" setup_wifi_ap
    ask_step "Setup python modules?" setup_python
    ask_step "Setup Adafruit DHT modules?" setup_AdafruitDHT
    ask_step "Setup INDI Dashboard?" setup_dashboard
    ask_step "Setup Shellinabox?" setup_shellinabox
    ask_step "Setup INDI Control Panel?" setup_indi_control_panel
}

