import time
class Camera:
    def __init__(self, name, indi_client):
        self.name = name
        self.indi_client = indi_client
        self.__find_device()
        self.__connect()
        self.__find_exposure_ctl()

    def shoot(self, exposure):
        self.ccd_exposure[0].value = exposure
        self.indi_client.sendNewNumber(self.ccd_exposure)

 

    def __find_device(self):
        self.device = None
        while not self.device:
            self.device = indi_client.getDevice(self.name)

    def __connect(self):
        if self.device.isConnected():
            return
        connect_property = None
        while not connect_property:
            connect_property = self.device.getSwitch("CONNECTION")
        connect_property[0].s=PyIndi.ISS_ON  # the "CONNECT" switch
        connect_property[1].s=PyIndi.ISS_OFF # the "DISCONNECT" switch
        self.indi_client.sendNewSwitch(connect_property) # send this new value to the device

    def __find_exposure_ctl(self):
        self.ccd_exposure = None
        while not(ccd_exposure):
            time.sleep(0.5)
            self.ccd_exposure=self.device.getNumber("CCD_EXPOSURE")


        

