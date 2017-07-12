from RPi import GPIO

class Passive:
    def __init__(self, gpio):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(gpio, GPIO.OUT)
        self.pwm = GPIO.PWM(gpio, 1)

    def play(self, frequency):
        self.pwm.stop()
        self.pwm.ChangeFrequency(frequency)
        self.pwm.start(50)

    def stop(self):
        self.pwm.stop()

