import time
from device import Device


class Camera(Device):
    def __init__(self, name, indi_client):
        Device.__init__(self, name, indi_client)
        self.connect()
        self.__find_exposure_ctl()

    def shoot(self, exposure):
        self.ccd_exposure[0].value = exposure
        self.indi_client.sendNewNumber(self.ccd_exposure)


    def __find_exposure_ctl(self):
        self.ccd_exposure = None
        while not(self.ccd_exposure):
            time.sleep(0.5)
            self.ccd_exposure=self.device.getNumber("CCD_EXPOSURE")


        

