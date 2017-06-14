from collections import OrderedDict
import time
import threading


class LedDisplay:
    def __init__(self):
        self.messages = OrderedDict()
        self.__last_index = -1
        self.__thread = threading.Thread(self.__rotate_messages)

    def add_message(self, key, message):
        self.messages[key] = message

    def remove_message(self, key):
        self.messages.pop(key)

    def __rotate_messages(self):
        while True:
            if len(self.messages) == 0:
                self.set_text('')
                time.sleep(0.5)
            else:
                self.__last_index = self.__last_index + 1 if self.__last_index < len(self.messages)-1 else 0
                message = [self.messages[m] for m in self.messages][self.__last_index]
                self.set_text(message['text'])
                time.sleep(message['duration'] if duration in message else 2)

