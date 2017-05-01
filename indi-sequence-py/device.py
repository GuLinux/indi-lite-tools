class Device:
    def __init__(self, name, indi_client):
        self.name = name
        self.indi_client = indi_client
        self.__find_device()

    def __find_device(self):
        self.device = None
        while not self.device:
            self.device = indi_client.getDevice(self.name)

    def connect(self):
        connect_property = None
        while not connect_property:
            connect_property = self.device.getSwitch("CONNECTION")

        if self.device.isConnected():
            return

        while not connect_property:
            connect_property = self.device.getSwitch("CONNECTION")
        connect_property[0].s=PyIndi.ISS_ON  # the "CONNECT" switch
        connect_property[1].s=PyIndi.ISS_OFF # the "DISCONNECT" switch
        self.indi_client.sendNewSwitch(connect_property) # send this new value to the device


