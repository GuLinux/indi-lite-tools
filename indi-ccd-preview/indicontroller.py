from indicamera import INDICamera
from indiclient import INDIClient
from astropy.io import fits
from datetime import datetime
import os
import scipy.misc
import numpy
import threading
import math
from glob import glob
import time
import pprint

class INDIImage:
    def __init__(self, workdir, fits_file, extension = 'jpg', log_y = True, bins = 256):
        self.fits_file = fits.open('/'.join([workdir, fits_file]))
        self.id = datetime.utcnow().isoformat()
        self.workdir = workdir
        self.extension = extension
        self.bins = bins
        self.__histogram()
        self.__save_image()

    def imagefile(self):
        return self.__filename('image')

    def __filename(self, name):
        return '{0}-{1}.{2}'.format(name, self.id, self.extension)

    def __path(self, name):
        return '{0}/{1}'.format(self.workdir, self.__filename(name))

    def __histogram(self):
        bins = self.bins
        # TODO: calculate absolute histogram, or relative to the values?
        # data_max = math.pow(2, int(self.fits_file[0].header['BITPIX'])) # TODO: this should be a bit more flexible, perhaps
        # steps = data_max / self.bins
        # bins = numpy.arange(0, data_max + 1, steps)
        self.hist = numpy.histogram(self.fits_file[0].data.flatten(), bins = bins)

    def __save_image(self):
        scipy.misc.imsave(self.__path('image'), self.fits_file[0].data)

class INDIController:
    __status = {'shooting': False}
    def __init__(self, workdir, format = 'jpg', bins = 256, log_y = True):
        self.client = INDIClient()
        self.format = format
        self.log_y = log_y
        self.bins = bins

        self.workdir = workdir
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
        INDIController.__status = {'shooting': True, 'exposure': exposure, 'started': time.time() }
        imager = INDICamera(device, self.client)
        if not imager.is_camera():
            raise RuntimeError('Device {0} is not an INDI CCD Camera'.format(device))
        imager.set_output(self.workdir, 'IMAGE_PREVIEW')
        imager.shoot(exposure)
        INDIController.__status = {'shooting': False, 'last_exposure': exposure, 'last_ended': time.time() }
        return INDIImage(self.workdir, 'IMAGE_PREVIEW.fits', bins=self.bins, log_y=self.log_y)

    def clean_cache(self):
        for file in glob(self.workdir + '/*'):
            os.remove(file)
        return len( [f for f in os.listdir(self.workdir) if os.isfile(f)] )    


    def status(self):
        return dict({'now': time.time(), **INDIController.__status })
