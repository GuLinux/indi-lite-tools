import datetime, time
from luma.core.render import canvas
from PIL import ImageFont
import threading

class OLed:
    def __init__(self, device):
        self.device = device
        self.message = {}
        self.__shown = {}
        self.__lock = threading.Lock()

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
        self.__lock.acquire()
        self.message['clock'] = time.strftime('%H:%M', time.gmtime())
        print('message={}, shown={}'.format(self.message, self.__shown))
        if self.message != self.__shown:
            self.__shown = self.message
            with canvas(self.device) as draw_canvas:
                self.__draw(draw_canvas, (90, 0), self.message['clock'], font_size=11)
                if 'title' in self.message:
                    self.__draw(draw_canvas, (0, 0), self.message['title'], font_size=11)
                if 'lines' in self.message:
                    start_y = 12
                    for line in self.message['lines']:
                        self.__draw(draw_canvas, (0, start_y), line, font_size=9)
                        start_y += 10
        self.__lock.release()

    def contrast(self, contrast):
        self.device.contrast(contrast)
                
    def __draw(self, draw_canvas, coords, text, font_size=8):
        font = ImageFont.truetype('DejaVuSans.ttf', font_size)
        draw_canvas.text(coords, text, fill='white', font=font)



