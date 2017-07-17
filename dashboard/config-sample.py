# Temp/Humidity sensor, comment if you don't have it
from sensors import AdafruitTempHumidity
import Adafruit_DHT

# Led segments (in this example, max7219)
from luma.core.render import canvas
from luma.core.virtual import sevensegment
from luma.led_matrix.device import max7219
from display import LumaLedMatrix
from buzzer import Buzzer, Passive as PassiveBuzzer
from luma.oled.device import sh1106
from luma.core.interface.serial import spi, i2c, noop
from display.oled import OLed


def setup(config):
    # Comment the config entries you don't have/need
    config['temp_humidity'] = AdafruitTempHumidity(Adafruit_DHT.AM2302, '4')
    config['temp_humidity_save_file'] = '/home/pi/temp_humidity.csv'
    config['temp_humidity_save_interval'] = 30

    #serial = spi(port=0, device=0, gpio=noop())
    #device = max7219(serial)
    #seg = sevensegment(device)
    #config['led_display'] = LumaLedMatrix(seg)

    serial = spi(device=0, port=0, gpio_DC=23, gpio_RST=24)
    oled_device = sh1106(serial)
    config['oled'] = OLed(oled_device)
    config['oled'].contrast(0)
    config['oled'].start_loop()

    config['buzzer'] = Buzzer(PassiveBuzzer(16))

class TestTempHumidity:
    def __init__(self):
        self.temp = 0
        self.humidity = 1

    def read(self):
        r = { 'humidity': self.humidity, 'temperature': self.temp }
        self.temp = self.temp+1
        self.humidity = self.humidity + 1
        return r

class TestLed:
    def __init__(self):
        self.message = None

    def set_message(self, message):
        self.message = message
        print('LED__TEXT__{}'.format(message))

    def remove_message(self):
        self.message = None

    def get_message(self):
        return self.message

def setup(config):
    # Comment the config entries you don't have/need
    config['led_display'] = TestLed()
    config['temp_humidity'] = TestTempHumidity()
    config['temp_humidity_save_file'] = '/home/marco/temp_humidity.csv'
    config['temp_humidity_save_interval'] = 30


# Configuration with OLED

#from luma.core.render import canvas
#from buzzer import Buzzer, Passive as PassiveBuzzer
#from luma.oled.device import sh1106
#from luma.core.interface.serial import spi, i2c, noop
#from display.oled import OLed
#
#import sys
#def setup(config):
#    serial = spi(device=0, port=0, gpio_DC=23, gpio_RST=24)
#    oled_device = sh1106(serial)
#    config['oled'] = OLed(oled_device)
#    config['oled'].contrast(0)
#    config['oled'].start_loop()
#
#    config['buzzer'] = Buzzer(PassiveBuzzer(26))

