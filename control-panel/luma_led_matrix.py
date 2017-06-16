# You need to pass an initialized led class to this object.
# Example:
# from luma.core.interface.serial import spi, noop
# from luma.core.render import canvas
# from luma.core.virtual import sevensegment
# from luma.led_matrix.device import max7219
# 
# serial = spi(port=0, device=0, gpio=noop())
# device = max7219(serial, cascaded=2)
# seg = sevensegment(device)
# led = LumaLedMatrix(seg)

class LumaLedMatrix():
    def __init__(self, led):
        self.led = led

    def set_message(self, message):
        self.led.text = str(message['text'])
        if 'brightness' in message:
            self.set_brightness(message['brightness'])

    def remove_message(self):
        self.led.text = ''

    def get_message(self):
        return self.led.text


    def set_brightness(self, brightness):
        self.led.device.contrast(brightness * 16)


