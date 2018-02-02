import PyIndi

    
class INDIClient(PyIndi.BaseClient):
    DEFAULT_HOST = 'localhost'
    DEFAULT_PORT = 7624

    def __init__(self, address=DEFAULT_HOST, port=DEFAULT_PORT, callbacks={}):
        PyIndi.BaseClient.__init__(self)
        self.host = address
        self.port = port
        self.setServer(address, port)
        self.callbacks = callbacks
        self.connectServer()

    @property
    def device_names(self):
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
        self.run_callback('serverConnected')        

    def serverDisconnected(self, code):
        self.run_callback('serverDisconnected', code)

    def run_callback(self, name, *args, **kwargs):
        callback = self.callbacks.get(name)
        if callback:
            callback(*args, **kwargs)

    def __str__(self):
        return 'INDI client connected to {0}:{1}'.format(self.host, self.port)

    def __repr__(self):
        return self.__str__()

