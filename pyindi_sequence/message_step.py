import time

class MessageStep:
    # message can be either a string, or a function returning a string

    def __init__(self, message, sleep_time = 0):
        self.message = message
        self.sleep_time = sleep_time

    def run(self):
        message = ""
        try:
            message = self.message()
        except:
            message = self.message
        print(message)
        if self.sleep_time > 0:
            time.sleep(self.sleep_time)
    
    def __str__(self):
        return 'Print message'

    def __repr__(self):
        return self.__str__()

 
