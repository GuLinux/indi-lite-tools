import datetime, time
from luma.core.render import canvas
from PIL import ImageFont

class OLed:
    def __init__(self, device):
        self.device = device
        self.message = {}
        self.__shown = {}

    def update(self, message):
        self.message.update(message)
        self.__redraw()

    def clear(self):
        self.message = {}
        self.__redraw()

    def __redraw(self):
        self.message['clock'] = time.strftime('%H:%M', time.gmtime())
        if self.message != self.__shown:
            self.__shown = self.message
            with canvas(self.device) as draw:
                self.__draw((80, 0), self.message['clock'], font_size=9)
                if 'title' in self.message:
                    self.__draw((0, 0), self.message['title'], font_size=9)
                if 'lines' in self.message:
                    start_y = 9
                    for line in self.message['lines']:
                        self.__draw((0, start_y), line, font_size=8)
                        start_y += 9

                
    def __draw(self, coords, text, font_size=8):
        font = ImageFont.truetype('DejaVuSans.ttf', 8)
        draw.text(coords, text, fill='white', font=font)



