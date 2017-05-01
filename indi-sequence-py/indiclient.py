import PyIndi
    
class INDIClient(PyIndi.BaseClient):
    def __init__(self, address = 'localhost', port = 7624):
        super(INDIClient, self).__init__()
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
        global blobEvent
        print("new BLOB ", bp.name)
        blobEvent.set()
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


