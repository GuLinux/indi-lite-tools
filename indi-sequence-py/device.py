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
            print('device {0} not found, retrying')

    def connect(self):
        if self.device.isConnected():
            return
        self.set_switch('CONNECTION', ['CONNECT'])

    def set_switch(self, name, on_switches = [], off_switches = [], sync = True):
        c = self.__getControl(name, 'switch')
        if c.r == PyIndi.ISR_ATMOST1 or c.r == PyIndi.ISR_1OFMANY:
            on_switches = on_switches[0:1]
            off_switches = [s.name for s in c if s.name not in on_switches]
        for index in range(0, len(c)):
            c[index].s = PyIndi.ISS_ON if c[index].name in on_switches else PyIndi.ISS_OFF
        self.indi_client.sendNewSwitch(c)

        if sync:
            self.__wait_for_ctl_status(c)

        return c
        
    def set_number(self, name, values, sync = True):
        c = self.__getControl(name, 'number')
        for control_name, index in self.__map_indexes(c, values.keys()).items():
            c[index].value = values[control_name]
        self.indi_client.sendNewNumber(c)

        if sync:
            self.__wait_for_ctl_status(c)
        return c

    def set_text(self, control_name, values, sync = True):
        c = self.__getControl(control_name, 'text')
        for control_name, index in self.__map_indexes(c, values.keys()).items():
            c[index].text = values[control_name]
        self.indi_client.sendNewText(c)

        if sync:
            self.__wait_for_ctl_status(c)

        return c
                
    def __wait_for_ctl_status(self, ctl, status = PyIndi.IPS_OK):
        while ctl.s != status:
            time.sleep(0.5)


    def __map_indexes(self, ctl, values):
        result = {}
        for i, c in enumerate(ctl):
             if c.name in values:
                result[c.name] = i
        return result


    def __getControl(self, name, ctl_type):
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
        return ctl

