import subprocess
import math


class INDIClient:


  def __init__(self, host = 'localhost', port = 7624):
    self.__host = host
    self.__port = port


  def get_properties(self, device='*', property='*', element='*'):
    return self.__parse_properties(self.__run_cmd('indi_getprop', ['{0}.{1}.{2}'.format(device, property, element)]))


  def set_property(self, device, property, element, value):
    self.__run_cmd('indi_setprop', ['{0}.{1}.{2}={3}'.format(device, property, element, value)])

  def set_property_sync(self, device, property, element, value, timeout=2):
    self.set_property(device, property, element, value)
    self.__run_cmd('indi_eval', ['-w', '-t', '{0}'.format(math.ceil(timeout)), '"{0}.{1}._STATE"==1'.format(device, property)])

  def __run_cmd(self, cmd, args):
    full_args = [cmd, '-h', self.__host, '-p', '{0}'.format(self.__port)] + args
    p = subprocess.Popen(full_args, stdout=subprocess.PIPE)
    #print(p.args)
    data = p.communicate()
    return (p.returncode, data[0])


  def __parse_properties(self, process_data):
    return [self.__parse_property(x) for x in process_data[1].decode('utf-8').split('\n') if x]


  def __parse_property(self, line):
    first = line.split('=')
    second = first[0].split('.')
    return {'device': second[0], 'property': second[1], 'element': second[2], 'value': first[1]}

