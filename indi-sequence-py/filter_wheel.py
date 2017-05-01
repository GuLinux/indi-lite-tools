from device import Device
import PyIndi

class FilterWheelStep:
    def __init__(self, filter_wheel, filter_name = None, filter_number = None):
        self.filter_wheel = filter_wheel

        if not filter_name and not filter_number:
            raise RuntimeError('One of filter name or number should be defined')
        if filter_name:
            self.filter_number = filter_wheel.filters()[filter_name]
            self.filter_name = filter_name
        else:
            self.filter_name = filter_wheel.filter_name(filter_number)
            self.filter_number = filter_number

    def run(self):
        self.filter_wheel.set_filter_number(self.filter_number)

    def __str__(self):
        return 'Change filter to {0} ({1}) on filter wheel {2}'.format(self.filter_name, self.filter_number, self.filter_wheel)

    def __repr__(self):
        return self.__str__()

    

class FilterWheel(Device):
    def __init__(self, name, indi_client, connect_on_create = True):
        Device.__init__(self, name, indi_client)
        if connect_on_create:
            self.connect()

    def set_filter(self, name):
       self.set_filter_number(self.filters()[name])

    def set_filter_number(self, number):
       self.set_number('FILTER_SLOT', {'FILTER_SLOT_VALUE': number})

    def filters(self):
        ctl = self.getControl('FILTER_NAME', 'text')
        filters = [(x.text, self.__name2number(x.name)) for x in ctl]
        return dict(filters)

    def current_filter(self):
        ctl = self.getControl('FILTER_SLOT', 'number')
        number = int(ctl[0].value)
        return number, self.filter_name(number)

    def filter_name(self, number):
        return [a for a, b in self.filters().items() if b == number][0]

    def __name2number(self, name):
        return int(name.replace('FILTER_SLOT_NAME_', ''))

    def __number2name(self, number):
        return 'FILTER_SLOT_NAME_{0}'.format(number)

    def __str__(self):
        filters = [(n, i) for n, i in self.filters().items()]
        filters.sort(key=lambda x: x[1])
        filters = ['{0} ({1})'.format(i[0], i[1]) for i in filters] 
        return 'FilterWheel {0}, current filter: {1}, available: {2}'.format(self.name, self.current_filter(), ', '.join(filters))

    def __repr__(self):
        return self.__str__()

