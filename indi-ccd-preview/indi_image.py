from datetime import datetime
from astropy.io import fits
import scipy.misc
import numpy
import math

class INDIImage:
    HIST_BINS = 'bins'
    HIST_LOGARITHMIC = 'logarithmic'
    HIST_ABSOLUTE = 'absolute'

    def __init__(self, workdir, fits_file, histogram_options, extension = 'jpg'):
        self.fits_file = fits.open('/'.join([workdir, fits_file]))
        self.id = datetime.utcnow().isoformat()
        self.workdir = workdir
        self.extension = extension
        self.histogram_options = histogram_options
        self.__histogram()
        self.__save_image()

    def imagefile(self):
        return self.__filename('image')

    def __filename(self, name):
        return '{0}-{1}.{2}'.format(name, self.id, self.extension)

    def __path(self, name):
        return '{0}/{1}'.format(self.workdir, self.__filename(name))

    def __histogram(self):
        bins = self.histogram_options[INDIImage.HIST_BINS]
        if self.histogram_options[INDIImage.HIST_ABSOLUTE]:
            data_max = math.pow(2, int(self.fits_file[0].header['BITPIX'])) # TODO: this should be a bit more flexible, perhaps
            steps = data_max / bins
            bins = numpy.arange(0, data_max + 1, steps)
        self.hist = numpy.histogram(self.fits_file[0].data.flatten(), bins = bins)

    def __save_image(self):
        scipy.misc.imsave(self.__path('image'), self.fits_file[0].data)

