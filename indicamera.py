
class INDICamera:
  def __init__(self, name, client):
    self.__cameraname = name
    self.__client = client

  def connect(self):
    self.set_property('CONNECTION', 'CONNECT', 'On')

  def disconnect(self):
    self.set_property('CONNECTION', 'DISCONNECT', 'On')

  def is_connected(self):
    return property('CONNECTION', 'CONNECT') == 'On'

  def output_dir(self):
    return property('UPLOAD_SETTINGS', 'UPLOAD_DIR')

  def output_prefix(self):
    return property('UPLOAD_SETTINGS', 'UPLOAD_PREFIX')

  def shoot(self, exposure):
    self.set_property('CCD_EXPOSURE', 'CCD_EXPOSURE_VALUE', exposure, exposure + 2)

  def set_output(self, path, prefix):
    self.set_property('UPLOAD_MODE', 'UPLOAD_LOCAL', 'On')
    self.set_property('UPLOAD_SETTINGS', 'UPLOAD_DIR', path)
    self.set_property('UPLOAD_SETTINGS', 'UPLOAD_PREFIX', prefix)


  def set_property(self, property, element, value, timeout = 2):
    self.__client.set_property_sync(self.__cameraname, property, element, value, timeout)

  def properties(self, property='*', element='*'): 
    return self.__client.get_properties(self.__cameraname, property, element)

  def property(self, property, element):
    return properties(property, element)[0]['value']

  def list(client):
    names = set([n['device'] for n in client.get_properties()])
    return [INDICamera(name, client) for name in names]
