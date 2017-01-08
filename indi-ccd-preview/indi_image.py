from datetime import datetime
from astropy.io import fits
import scipy.misc
import numpy
import math

class INDIImage:
    def __init__(self, workdir, fits_file, extension = 'jpg', log_y = True, bins = 256, histogram_absolute = False):
        self.fits_file = fits.open('/'.join([workdir, fits_file]))
        self.id = datetime.utcnow().isoformat()
        self.workdir = workdir
        self.extension = extension
        self.bins = bins
        self.histogram_absolute = histogram_absolute
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
        if self.histogram_absolute:
            data_max = math.pow(2, int(self.fits_file[0].header['BITPIX'])) # TODO: this should be a bit more flexible, perhaps
            steps = data_max / self.bins
            bins = numpy.arange(0, data_max + 1, steps)
        self.hist = numpy.histogram(self.fits_file[0].data.flatten(), bins = bins)

    def __save_image(self):
        scipy.misc.imsave(self.__path('image'), self.fits_file[0].data)

