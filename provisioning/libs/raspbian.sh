
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

install_indi() {
    mkdir /tmp/indi_install
    cd /tmp/indi_install
    wget "indilib.org/jdownloads/Raspberry PI/libindi_1.5.0_rpi.tar.gz"
    tar xf "libindi_1.5.0_rpi.tar.gz"
    dpkg -i libindi*/*.deb
    cd -
    rm -rf /tmp/indi_install
}


full_upgrade() {
	apt-get update && apt-get dist-upgrade -y
}

install_prerequisites() {
    apt-get update && apt-get install -y cdbs libcfitsio3-dev libnova-dev libusb-1.0-0-dev libjpeg-dev \
        libusb-dev libtiff5-dev libftdi-dev fxload libkrb5-dev libcurl4-gnutls-dev libraw-dev libgphoto2-dev \
        libgsl0-dev dkms libboost-regex-dev libgps-dev libdc1394-22-dev vim curl wget nginx \
        ${python_pkgname}-pip i${python_pkgname} ${python_pkgname}-dev git hostapd tmux dnsmasq swig shellinabox libfreetype6-dev fonts-dejavu-core 
}


install_distro_steps() {
    ask_step "Upgrade packages?" full_upgrade
    ask_step "Enable ssh on boot?" enable_ssh
    ask_step "Install dependencies?" install_prerequisites
    ask_step "Install latest INDI?" install_indi
    ask_step "Enable SPI interface?" enable_spi
    ask_step "Enable GPIO/I2C hwclock support?" enable_hwclock
    ask_step "Disable audio?" disable_audio
    ask_step "Setup shell environment?" setup_shell
    ask_step "Setup nginx?" setup_nginx
    ask_step "Setup wifi access point?" setup_wifi_ap
    ask_step "Setup python modules?" setup_python
    ask_step "Setup Adafruit DHT modules?" setup_AdafruitDHT
    ask_step "Setup INDI Dashboard?" setup_dashboard
    ask_step "Setup HDMI control?" setup_hdmi
    ask_step "Setup Shellinabox?" setup_shellinabox
    ask_step "Setup INDI Control Panel?" setup_indi_control_panel
}

