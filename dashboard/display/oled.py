import datetime, time
from luma.core.render import canvas
from PIL import ImageFont
import threading

class OLed:
    def __init__(self, device):
        self.device = device
        self.message = {}
        self.__shown = {}

    def update(self, message):
        self.message = message
        self.__redraw()

    def clear(self):
        self.message = {}
        self.__redraw()

    def start_loop(self):
        self.__loop = True
        self.__thread = threading.Thread(target=self.__thread_loop)
        self.__thread.start()


    def stop_loop(self):
        self.__loop = False

    def __thread_loop(self):
        while self.__loop:
            self.__redraw()
            time.sleep(1)

    def __redraw(self):
        self.message['clock'] = time.strftime('%H:%M', time.gmtime())
        if self.message != self.__shown:
            self.__shown = self.message.copy()
            with canvas(self.device) as draw_canvas:
                start_y = self.__draw(draw_canvas, (90, 0), self.message['clock'], font_size=11)[1]
                if 'title' in self.message:
                    self.__draw(draw_canvas, (0, 0), self.message['title'], font_size=11)
                if 'text' in self.message:
                    self.__draw(draw_canvas, (0, start_y), self.message['text'], font_size=9)

    def contrast(self, contrast):
        self.device.contrast(contrast)
                
    def __draw(self, draw_canvas, coords, text, font_size=8):
        font = ImageFont.truetype('DejaVuSans.ttf', font_size)
        draw_canvas.multiline_text(coords, text, fill='white', font=font)
        return draw_canvas.multiline_textsize(text, font)



