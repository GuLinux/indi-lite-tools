import PyIndi
from .device import Device
from .camera import Camera
from .filter_wheel import FilterWheel

    
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

    def cameras(self):
       return [Camera(x, self) for x in self.__devices_by_interface('ccd')]

    def filter_wheels(self):
       return [FilterWheel(x, self) for x in self.__devices_by_interface('filter')]

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

    def __devices_by_interface(self, interface):
        devices = [Device(x, self) for x in self.device_names]
        return [x.name for x in devices if interface in x.interfaces]
 

    def __str__(self):
        return 'INDI client connected to {0}:{1}'.format(self.host, self.port)

    def __repr__(self):
        return self.__str__()

