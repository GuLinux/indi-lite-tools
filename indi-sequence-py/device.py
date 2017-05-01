import PyIndi
import time

class Device:
    def __init__(self, name, indi_client):
        self.name = name
        self.indi_client = indi_client
        self.__find_device()

    def __find_device(self):
        self.device = None
        while not self.device:
            self.device = self.indi_client.getDevice(self.name)

    def connect(self):
        connect_property = self.__getControl('switch', 'CONNECTION')
        if self.device.isConnected():
            return
        connect_property[0].s=PyIndi.ISS_ON  # the "CONNECT" switch
        connect_property[1].s=PyIndi.ISS_OFF # the "DISCONNECT" switch
        self.indi_client.sendNewSwitch(connect_property) # send this new value to the device


    def __getControl(self, ctl_type, name):
        ctl = None
        attr = {
            'number': 'getNumber',
            'switch': 'getSwitch',
            'text': 'getText',
            'blob': 'getBlob'
        }[ctl_type]
        while not(ctl):
            ctl = getattr(self.device, attr)(name)
            time.sleep(0.1)

