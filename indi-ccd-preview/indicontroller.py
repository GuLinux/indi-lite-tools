from indicamera import INDICamera
from indiclient import INDIClient
import os
from glob import glob
import time
from indi_image import INDIImage

class INDIController:
    __status = {'shooting': False}
    def __init__(self, app ):
        self.app = app
        self.client = INDIClient()
        self.workdir = app.static_folder + '/images'
        self.histogram_options = { INDIImage.HIST_BINS: 256, INDIImage.HIST_LOGARITHMIC: True, INDIImage.HIST_ABSOLUTE: False } 
        if not os.path.isdir(self.workdir):
            os.makedirs(self.workdir)

    def devices(self):
        properties = self.client.get_properties()
        devices = list(set([property['device'] for property in properties]))
        result = {}
        for device in devices:
            result[device] = [p for p in properties if p['device'] == device]
        return result

    def device_names(self):
        properties = self.client.get_properties()
        devices = list(set([property['device'] for property in properties]))
        devices.sort()
        return devices

    def properties(self, device):
       return self.client.get_properties(device) 

    def property(self, device, property):
        property_element = property.split('.')
        return self.client.get_properties(device, property_element[0], property_element[1])[0]

    def set_property(self, device, property, value):
        property_element = property.split('.')
        self.client.set_property_sync(device, property_element[0], property_element[1], value)
        return self.property(device, property)

    def preview(self, device, exposure):
        if INDIController.__status['shooting']:
            raise RuntimeError('Anoter exposure is already in progress')
        imager = INDICamera(device, self.client)
        if not imager.is_camera():
            raise RuntimeError('Device {0} is not an INDI CCD Camera'.format(device))
        INDIController.__status = {'shooting': True, 'exposure': exposure, 'started': time.time() }
        imager.set_output(self.workdir, 'IMAGE_PREVIEW')
        imager.shoot(exposure)
        INDIController.__status = {'shooting': False, 'last_exposure': exposure, 'last_ended': time.time() }
        return INDIImage(self.workdir, 'IMAGE_PREVIEW.fits', self.histogram_options, extension=self.app.config['image_format'])

    def clean_cache(self):
        for file in glob(self.workdir + '/*'):
            os.remove(file)
        return len( [f for f in os.listdir(self.workdir) if os.isfile(f)] )    


    def status(self):
        status ={'now': time.time()}
        status.update(INDIController.__status)
        return status

    def set_histogram_settings(self, data):
        self.histogram_options = data

