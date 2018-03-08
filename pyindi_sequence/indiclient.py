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
        self.run_callback('on_new_device', d)

    def newProperty(self, p):
        self.run_callback('on_new_property', p)

    def removeProperty(self, p):
        self.run_callback('on_remove_property', p)

    def newBLOB(self, bp):
        self.run_callback('on_new_blob', bp)

    def newSwitch(self, svp):
        self.run_callback('on_new_switch', svp)

    def newNumber(self, nvp):
        self.run_callback('on_new_number', nvp)

    def newText(self, tvp):
        self.run_callback('on_new_text', tvp)

    def newLight(self, lvp):
        self.run_callback('on_new_light', lvp)

    def newMessage(self, d, m):
        self.run_callback('on_new_message', d, m)

    def serverConnected(self):
        self.run_callback('on_server_connected')        

    def serverDisconnected(self, code):
        self.run_callback('on_server_disconnected', code)

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

