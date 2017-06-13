# Temp/Humidity sensor, comment if you don't have it
from adafruit_temp_humidity import AdafruitTempHumidity, Adafruit_DHT


def setup(config):
    # Comment the config entries you don't have/need
    config['temp_humidity'] = AdafruitTempHumidity(Adafruit_DHT.AM2302, '4')

