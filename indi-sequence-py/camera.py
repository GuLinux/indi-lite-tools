import time
from device import Device
import PyIndi


class Camera(Device):
    def __init__(self, name, indi_client):
        Device.__init__(self, name, indi_client)
        self.connect()

    def shoot(self, exposure, sync = True):
        ctl = self.set_number('CCD_EXPOSURE', exposure)
        if sync:
            while ctl.s != PyIndi.IPS_OK:
                time.sleep(0.5)
        return ctl 

