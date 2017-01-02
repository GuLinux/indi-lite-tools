from indicamera import INDICamera
from indiclient import INDIClient
from astropy.io import fits
from datetime import datetime
import os
import scipy.misc
import numpy
import matplotlib.pyplot as plt
from glob import glob
import pprint

class ImageFiles:
    def __init__(self, workdir, extension = 'jpg'):
        self.timestamp = datetime.utcnow().isoformat()
        self.workdir = workdir
        self.extension = extension

    def filename(self, name):
        return '{0}-{1}.{2}'.format(name, self.timestamp, self.extension)

    def path(self, name):
        return '{0}/{1}'.format(self.workdir, self.filename(name))

    def glob(self, name):
        return glob('{0}/{1}-*.{2}'.format(self.workdir, name, self.extension))

class INDIController:
    def __init__(self, workdir):
        self.client = INDIClient()

        self.workdir = '{0}/images'.format(workdir)
        if not os.path.isdir(self.workdir):
            os.makedirs(self.workdir)


    def devices(self):
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
        images = ImageFiles(self.workdir)
        fits_data = self.__shoot(device, exposure)

        scipy.misc.imsave(images.path('preview'), fits_data)
        self.__make_histogram(fits_data, images.path('histogram'))

        # self.__clean(images, ['preview', 'histogram'])
        return 'images/' + images.filename('preview'), 'images/' + images.filename('histogram')

    def __shoot(self, device, exposure):
        imager = INDICamera(device, self.client)
        if not imager.is_camera():
            raise RuntimeError('Device {0} is not an INDI CCD Camera'.format(device))
        imager.set_output(self.workdir, 'IMAGE_PREVIEW')
        imager.shoot(exposure)
        fits_data = fits.getdata(self.workdir + '/IMAGE_PREVIEW.fits')
        return fits_data



    def __make_histogram(self, data, filename, log_y = True, bins = 256):
        plt.clf()
        plt.hist(data.flatten() , bins=256)
        plt.xlim([0, 255])
        if log_y:
            plt.yscale('log')
        plt.savefig(filename)

    def __clean(self, images, names):
        for name in names:
            for file in images.glob(name)[:-3]:
                os.remove(file)

