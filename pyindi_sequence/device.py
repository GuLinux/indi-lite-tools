import PyIndi
import time

class Device:
    DEFAULT_TIMEOUT = 30

    def __init__(self, name, indi_client):
        self.name = name
        self.indi_client = indi_client
        self.__find_device()
        self.timeout = Device.DEFAULT_TIMEOUT

    def __find_device(self):
        self.device = None
        while not self.device:
            self.device = self.indi_client.getDevice(self.name)

    def connect(self):
        if self.device.isConnected():
            return
        self.set_switch('CONNECTION', ['CONNECT'])

    def values(self, ctl_name, ctl_type):
        return dict(map(lambda c: (c.name, c.value), self.getControl(ctl_name, ctl_type)))

    def switch_values(self, switch_name):
        return dict(map(lambda sw: (sw.name, sw.s == PyIndi.ISS_ON), self.getControl(switch_name, 'switch')))

    def set_switch(self, name, on_switches = [], off_switches = [], sync = True, timeout=None):
        c = self.getControl(name, 'switch')
        if c.r == PyIndi.ISR_ATMOST1 or c.r == PyIndi.ISR_1OFMANY:
            on_switches = on_switches[0:1]
            off_switches = [s.name for s in c if s.name not in on_switches]
        for index in range(0, len(c)):
            c[index].s = PyIndi.ISS_ON if c[index].name in on_switches else PyIndi.ISS_OFF
        self.indi_client.sendNewSwitch(c)

        if sync:
            self.__wait_for_ctl_statuses(c, statuses=[PyIndi.IPS_IDLE, PyIndi.IPS_OK], timeout=timeout)

        return c
        
    def set_number(self, name, values, sync = True, timeout=None):
        c = self.getControl(name, 'number')
        for control_name, index in self.__map_indexes(c, values.keys()).items():
            c[index].value = values[control_name]
        self.indi_client.sendNewNumber(c)

        if sync:
            self.__wait_for_ctl_statuses(c, timeout=timeout)
        return c

    def set_text(self, control_name, values, sync = True, timeout=None):
        c = self.getControl(control_name, 'text')
        for control_name, index in self.__map_indexes(c, values.keys()).items():
            c[index].text = values[control_name]
        self.indi_client.sendNewText(c)

        if sync:
            self.__wait_for_ctl_statuses(c, timeout=timeout)

        return c

    def __wait_for_ctl_statuses(self, ctl, statuses=[PyIndi.IPS_OK, PyIndi.IPS_IDLE], timeout=None):
        started = time.time()
        if timeout is None:
            timeout = self.timeout
        while ctl.s not in statuses:
            if 0 < timeout < time.time() - started:
                raise RuntimeError('Timeout error while changing property {}'.format(ctl.name))
            time.sleep(0.01)

    def __map_indexes(self, ctl, values):
        result = {}
        for i, c in enumerate(ctl):
             if c.name in values:
                result[c.name] = i
        return result

    def getControl(self, name, ctl_type, timeout=None):
        ctl = None
        attr = {
            'number': 'getNumber',
            'switch': 'getSwitch',
            'text': 'getText',
            'blob': 'getBlob'
        }[ctl_type]
        if timeout is None:
            timeout = self.timeout
        started = time.time()
        while not(ctl):
            ctl = getattr(self.device, attr)(name)
            if not ctl and 0 < timeout < time.time() - started:
                raise RuntimeError('Timeout finding control {}'.format(name))
            time.sleep(0.01)
        return ctl

    def has_control(self, name, ctl_type):
        try:
            self.getControl(name, ctl_type, timeout=0.1)
            return True
        except:
            return False

