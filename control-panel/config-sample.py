# Temp/Humidity sensor, comment if you don't have it
from adafruit_temp_humidity import AdafruitTempHumidity

def setup(config):
    # Comment the config entries you don't have/need
    config['temp_humidity'] = AdafruitTempHumidity('2302', '4')

