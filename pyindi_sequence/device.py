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
        self.__switch_types = { PyIndi.ISR_1OFMANY: 'ONE_OF_MANY', PyIndi.ISR_ATMOST1: 'AT_MOST_ONE', PyIndi.ISR_NOFMANY: 'ANY'}
        self.__type_to_str = { PyIndi.INDI_NUMBER: 'number', PyIndi.INDI_SWITCH: 'switch', PyIndi.INDI_TEXT: 'text', PyIndi.INDI_LIGHT: 'light', PyIndi.INDI_BLOB: 'blob', PyIndi.INDI_UNKNOWN: 'unknown' }
        self.interfaces = Device.find_interfaces(self.device)

    def __find_device(self):
        self.device = None
        while not self.device:
            self.device = self.indi_client.getDevice(self.name)

    @property
    def connected(self):
        return self.device.isConnected()

    def connect(self):
        if self.connected:
            return
        self.set_switch('CONNECTION', ['CONNECT'])

    def values(self, ctl_name, ctl_type):
        return dict(map(lambda c: (c.name, c.value), self.get_control(ctl_name, ctl_type)))
       

    def switch_values(self, name, ctl = None):
        return self.__control2dict(name, 'switch', lambda c: {'value': c.s == PyIndi.ISS_ON}, ctl)

    def text_values(self, name, ctl = None):
        return self.__control2dict(name, 'text', lambda c: {'value': c.text}, ctl)

    def number_values(self, name, ctl = None):
        return self.__control2dict(name, 'text', lambda c: {'value': c.value, 'min': c.min, 'max': c.max, 'step': c.step, 'format': c.format}, ctl)

    def light_values(self, name, ctl = None):
        return self.__control2dict(name, 'light', lambda c: {'value': self.__state_to_str[c.s]}, ctl)


    def __control2dict(self, control_name, control_type, transform, control = None):
        def get_dict(element):
            dest = {'name': element.name, 'label': element.label}
            dest.update(transform(element))
            return dest

        control = control if control else self.get_control(control_name, control_type)
        return [ get_dict(c) for c in control]

    def set_switch(self, name, on_switches = [], off_switches = [], sync = True, timeout=None):
        c = self.get_control(name, 'switch')
        is_exclusive = c.r == PyIndi.ISR_ATMOST1 or c.r == PyIndi.ISR_1OFMANY
        if is_exclusive :
            on_switches = on_switches[0:1]
            off_switches = [s.name for s in c if s.name not in on_switches]
        for index in range(0, len(c)):
            current_state = c[index].s
            new_state = current_state
            if c[index].name in on_switches:
                new_state = PyIndi.ISS_ON
            elif is_exclusive or c[index].name in off_switches:
                new_state = PyIndi.ISS_OFF
            c[index].s = new_state
        self.indi_client.sendNewSwitch(c)

        if sync:
            self.__wait_for_ctl_statuses(c, statuses=[PyIndi.IPS_IDLE, PyIndi.IPS_OK], timeout=timeout)

        return c
        
    def set_number(self, name, values, sync = True, timeout=None):
        c = self.get_control(name, 'number')
        for control_name, index in self.__map_indexes(c, values.keys()).items():
            c[index].value = values[control_name]
        self.indi_client.sendNewNumber(c)

        if sync:
            self.__wait_for_ctl_statuses(c, timeout=timeout)
        return c

    def set_text(self, control_name, values, sync = True, timeout=None):
        c = self.get_control(control_name, 'text')
        for control_name, index in self.__map_indexes(c, values.keys()).items():
            c[index].text = values[control_name]
        self.indi_client.sendNewText(c)

        if sync:
            self.__wait_for_ctl_statuses(c, timeout=timeout)

        return c
    
    @staticmethod
    def find_interfaces(indidevice):
        interface = indidevice.getDriverInterface()
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

    def __wait_for_ctl_statuses(self, ctl, statuses=[PyIndi.IPS_OK, PyIndi.IPS_IDLE], timeout=None):
        started = time.time()
        if timeout is None:
            timeout = self.timeout
        while ctl.s not in statuses:
            # print('{}/{}/{}: {}'.format(ctl.device, ctl.group, ctl.name, self.__state_to_str[ctl.s]))
            if ctl.s == PyIndi.IPS_ALERT and 0.5 > time.time() - started:
                raise RuntimeError('Error while changing property {}'.format(ctl.name))
            elapsed = time.time() - started
            if 0 < timeout < elapsed:
                raise RuntimeError('Timeout error while changing property {}: elapsed={}, timeout={}, status={}'.format(ctl.name, elapsed, timeout, self.__state_to_str[ctl.s] ))
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

    def get_property(self, name):
        indi_property = self.device.getProperty(name)
        return self.__read_property(indi_property) if indi_property else None

    def get_queued_message(self, index):
        message = self.device.messageQueue(index)
        message.acquire()
        # TODO: this might be a bit hacky
        message_string = ctypes.cast(message.__int__(), ctypes.POINTER(ctypes.c_char_p)).contents.value.decode('utf-8')
        message.disown()
        return message_string


    def __read_property(self, p):
        name = p.getName()
        base_dict = { 'name': name, 'label': p.getLabel(), 'group': p.getGroupName(), 'device': p.getDeviceName(), 'type': self.__type_to_str[p.getType()], 'state': self.__state_to_str[p.getState()]}
        permission = p.getPermission()
        base_dict['perm_read'] = permission in [PyIndi.IP_RO, PyIndi.IP_RW]
        base_dict['perm_write'] = permission in [PyIndi.IP_WO, PyIndi.IP_RW]
        control = self.get_control(base_dict['name'], base_dict['type'])

        if p.getType() == PyIndi.INDI_NUMBER:
            base_dict['values'] = self.number_values(name, control)
        elif p.getType() == PyIndi.INDI_SWITCH:
            base_dict['rule'] = self.__switch_types[control.r]
            base_dict['values'] = self.switch_values(name, control)
        elif p.getType() == PyIndi.INDI_TEXT:
            base_dict['values'] = self.text_values(name, control)
        elif p.getType() == PyIndi.INDI_LIGHT:
            base_dict['values'] = self.light_values(name, control)
        return base_dict

    def get_control(self, name, ctl_type, timeout=None):
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
            self.get_control(name, ctl_type, timeout=0.1)
            return True
        except:
            return False

