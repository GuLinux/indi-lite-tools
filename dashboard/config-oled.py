# Configuration with OLED

from luma.core.render import canvas
from buzzer import Buzzer, Passive as PassiveBuzzer
from luma.oled.device import sh1106
from luma.core.interface.serial import spi, i2c, noop
from display.oled import OLed

import sys
def setup(config):
    serial = spi(device=0, port=0, gpio_DC=23, gpio_RST=24)
    oled_device = sh1106(serial)
    config['oled'] = OLed(oled_device)
    config['oled'].contrast(0)
    config['oled'].start_loop()

    config['buzzer'] = Buzzer(PassiveBuzzer(26))

