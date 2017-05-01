import time
from device import Device


class Camera(Device):
    def __init__(self, name, indi_client):
        Device.__init__(self, name, indi_client)
        self.connect()

    def shoot(self, exposure):
        self.set_number('CCD_EXPOSURE', exposure)


        

