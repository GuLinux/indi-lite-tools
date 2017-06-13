import Adafruit_DHT

# constructor argument as per https://github.com/adafruit/Adafruit_Python_DHT/blob/master/examples/AdafruitDHT.py
class AdafruitTempHumidity:
    def __init__(self, sensor, pin):
        self.sensor = sensor
        self.pin = pin

    def read(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)
        return { 'humidity': humidity, 'temperature': temperature }
