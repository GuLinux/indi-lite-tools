# Temp/Humidity sensor, comment if you don't have it
from adafruit_temp_humidity import AdafruitTempHumidity, Adafruit_DHT

# Led segments (in this example, max7219)
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import sevensegment
from luma.led_matrix.device import max7219
from luma_led_matrix import LumaLedMatrix


def setup(config):
    # Comment the config entries you don't have/need
    config['temp_humidity'] = AdafruitTempHumidity(Adafruit_DHT.AM2302, '4')
    config['temp_humidity_save_file'] = '/home/pi/temp_humidity.csv'
    config['temp_humidity_save_interval'] = 30

    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial)
    seg = sevensegment(device)
    config['led_display'] = LumaLedMatrix(seg)


