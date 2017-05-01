import PyIndi

    
class INDIClient(PyIndi.BaseClient):
    DEFAULT_HOST = 'localhost'
    DEFAULT_PORT = 7624

    def __init__(self, address = DEFAULT_HOST, port = DEFAULT_PORT):
        super(INDIClient, self).__init__()
        self.host = address
        self.port = port
        self.setServer(address, port)
        self.connectServer()

    def listDeviceNames(self):
        return [d.getDeviceName() for d in self.getDevices()]
            

    def newDevice(self, d):
        pass

    def newProperty(self, p):
        pass

    def removeProperty(self, p):
        pass

    def newBLOB(self, bp):
        pass

    def newSwitch(self, svp):
        pass

    def newNumber(self, nvp):
        pass

    def newText(self, tvp):
        pass

    def newLight(self, lvp):
        pass

    def newMessage(self, d, m):
        pass

    def serverConnected(self):
        pass

    def serverDisconnected(self, code):
        pass

    def __str__(self):
        return 'INDI client connected to {0}:{1}'.format(self.host, self.port)

    def __repr__(self):
        return self.__str__()

