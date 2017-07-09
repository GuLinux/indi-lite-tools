import time
import threading
import functools

class Buzzer:
    DEFAULT_PATTERN = [{'frequency': 1000, 'duration': 0.5}, {'frequency': 0, 'duration': 0.5}]
    def __init__(self, driver):
        self.driver = driver
        self.__thread = None

    def start(self, settings):
        self.stop()
        pattern = settings.get('pattern', Buzzer.DEFAULT_PATTERN)
        loop = settings.get('loop', True)
        max_duration = settings.get('duration')
        self.__thread = threading.Thread(target=self.__play_pattern, args=(pattern, loop, max_duration))
        self.__thread.start()

    def stop(self):
        self.__running = False
        if self.__thread:
            self.__thread.join()
            self.__thread = None

    def __play_pattern(self, pattern, loop=True, max_duration=None):
        index = -1
        self.__running = True
        started = time.time()
        while self.__running and (max_duration is None or time.time() - started < max_duration):
            index += 1
            if index >= len(pattern):
                if loop:
                    index = 0
                else:
                    return

            pattern_entry = pattern[index]
            frequency = pattern_entry.get('frequency', 1000)
            duration = pattern_entry.get('duration', 0.5)
            self.__play(frequency, duration)
        self.driver.stop()

    def __play(self, frequency, duration):
        if frequency > 0:
            self.driver.play(frequency)
        time.sleep(duration)
        self.driver.stop()

    def __stop(self):
        self.driver.stop()
