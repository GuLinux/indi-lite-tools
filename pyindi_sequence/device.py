import PyIndi
import time
import ctypes


class Device:
    DEFAULT_TIMEOUT = 30

    def __init__(self, name, indi_client):
        self.name = name
        self.indi_client = indi_client
        self.__find_device()
        self.timeout = Device.DEFAULT_TIMEOUT

        self.__state_to_str = { PyIndi.IPS_IDLE: 'IDLE', PyIndi.IPS_OK: 'OK', PyIndi.IPS_BUSY: 'BUSY', PyIndi.IPS_ALERT: 'ALERT' }
        self.__type_to_str = { PyIndi.INDI_NUMBER: 'number', PyIndi.INDI_SWITCH: 'switch', PyIndi.INDI_TEXT: 'text', PyIndi.INDI_LIGHT: 'light', PyIndi.INDI_BLOB: 'blob', PyIndi.INDI_UNKNOWN: 'unknown' }

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

    @property
    def interfaces(self):
        interface = self.device.getDriverInterface()
        interface.acquire()
        device_interfaces = int(ctypes.cast(interface.__int__(), ctypes.POINTER(ctypes.c_uint16)).contents.value)
        interface.disown()
        interfaces = {
            PyIndi.BaseDevice.GENERAL_INTERFACE: 'general', 
            PyIndi.BaseDevice.TELESCOPE_INTERFACE: 'telescope',
            PyIndi.BaseDevice.CCD_INTERFACE: 'ccd',
            PyIndi.BaseDevice.GUIDER_INTERFACE: 'guider',
            PyIndi.BaseDevice.FOCUSER_INTERFACE: 'focuser',
            PyIndi.BaseDevice.FILTER_INTERFACE: 'filter',
            PyIndi.BaseDevice.DOME_INTERFACE: 'dome',
            PyIndi.BaseDevice.GPS_INTERFACE: 'gps',
            PyIndi.BaseDevice.WEATHER_INTERFACE: 'weather',
            PyIndi.BaseDevice.AO_INTERFACE: 'ao',
            PyIndi.BaseDevice.DUSTCAP_INTERFACE: 'dustcap',
            PyIndi.BaseDevice.LIGHTBOX_INTERFACE: 'lightbox',
            PyIndi.BaseDevice.DETECTOR_INTERFACE: 'detector',
            PyIndi.BaseDevice.ROTATOR_INTERFACE: 'rotator',
            PyIndi.BaseDevice.AUX_INTERFACE: 'aux'
        }
        interfaces = [interfaces[x] for x in interfaces if x & device_interfaces]
        return interfaces
        

    def switch_values(self, name, ctl = None):
        return self.__control2dict(name, 'switch', lambda c: {'value': c.s == PyIndi.ISS_ON}, ctl)

    def text_values(self, name, ctl = None):
        return self.__control2dict(name, 'text', lambda c: {'value': c.text}, ctl)

    def number_values(self, name, ctl = None):
        return self.__control2dict(name, 'text', lambda c: {'value': c.value, 'min': c.min, 'max': c.max, 'step': c.step, 'format': c.format}, ctl)

    def light_values(self, name, ctl = None):
        return self.__control2dict(name, 'text', lambda c: {'value': self.__state_to_str[c.s]}, ctl)


    def __control2dict(self, control_name, control_type, transform, control = None):
        def get_dict(element):
            dest = {'name': element.name, 'label': element.label}
            dest.update(transform(element))
            return dest

        control = control if control else self.getControl(control_name, control_type)
        return [ get_dict(c) for c in control]

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

    def get_properties(self):
        properties = self.device.getProperties()
        return [ self.__read_property(p) for p in properties]

    def __read_property(self, p):
        name = p.getName()
        base_dict = { 'name': name, 'label': p.getLabel(), 'group': p.getGroupName(), 'device': p.getDeviceName(), 'type': self.__type_to_str[p.getType()], 'state': self.__state_to_str[p.getState()]}
        control = self.getControl(base_dict['name'], base_dict['type'])

        if p.getType() == PyIndi.INDI_NUMBER:
            base_dict['values'] = self.number_values(name, control)
        elif p.getType() == PyIndi.INDI_SWITCH:
            base_dict['values'] = self.switch_values(name, control)
        elif p.getType() == PyIndi.INDI_TEXT:
            base_dict['values'] = self.text_values(name, control)
        elif p.getText() == PyIndi.INDI_LIGHT:
            base_dict['values'] = self.light_values(name, control)
        return base_dict

    def getControl(self, name, ctl_type, timeout=None):
        ctl = None
        attr = {
            'number': 'getNumber',
            'switch': 'getSwitch',
            'text': 'getText',
            'light': 'getLight',
            'blob': 'getBLOB'
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

