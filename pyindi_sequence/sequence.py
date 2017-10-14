import os, time
from astropy.io import fits
import shutil


class SequenceCallbacks:
    def __init__(self, **kwargs):
        self.callbacks = kwargs

    def add(self, name, callback):
        if name not in self.callbacks:
            self.callbacks[name] = []
        self.callbacks[name].append(callback)

    def run(self, name, *args, **kwargs):
        if name not in self.callbacks:
            return
        for callback in self.callbacks[name]:
            callback(*args, **kwargs)


class Sequence:
    def __init__(self, camera, name, exposure, count, upload_path, start_index=1, **kwargs):
        self.camera = camera
        self.name = name
        self.count = count
        self.exposure = exposure
        self.upload_path = upload_path
        self.callbacks = SequenceCallbacks(**kwargs)
        self.finished = 0
        self.start_index = start_index
        if not os.path.isdir(upload_path):
            os.makedirs(upload_path)

    def run(self):
        self.camera.set_upload_to('local')
        sequence_prefix='{0}_{1}s_'.format(self.name, self.exposure)
        tmp_prefix = sequence_prefix + 'TMP'
        tmp_file = os.path.join(self.upload_path, tmp_prefix + '.fits')

        self.camera.set_upload_path(self.upload_path, tmp_prefix)
        self.callbacks.run('on_started', self)

        for sequence in range(0, self.count):
            self.callbacks.run('on_each_started', self, sequence)
            # Check for 'pause' file
            while os.path.isfile(os.path.join(self.upload_path, 'pause')):
                time.sleep(0.5)

            temp_before = self.ccd_temperature
            self.camera.shoot(self.exposure)
            temp_after = self.ccd_temperature

            file_name = os.path.join(self.upload_path, '{0}{1:03}.fits'.format(sequence_prefix, sequence+self.start_index))
            shutil.move(tmp_file, file_name)

            if temp_before is not None and temp_after is not None:
                temp_avg = (temp_before + temp_after) / 2
                fits_file = fits.open(file_name, mode='append')
                if 'CCD-TEMP' not in fits_file[0].header:
                    fits_file[0].header['CCD-TEMP'] = (temp_avg, 'CCD Temperature (Celsius)')
                    fits_file.writeto(file_name, overwrite=True)
                fits_file.close()

            self.finished += 1
            self.callbacks.run('on_each_finished', self, sequence, file_name)

        self.callbacks.run('on_finished', self)

    @property
    def ccd_temperature(self):
        if self.camera.has_control('CCD_TEMPERATURE', 'number'):
            return self.camera.values('CCD_TEMPERATURE', 'number')['CCD_TEMPERATURE_VALUE']
        return None
        
    @property
    def total_seconds(self):
        return self.exposure * self.count

    @property
    def shot_seconds(self):
        return self.finished * self.exposure

    @property
    def remaining_seconds(self):
        return self.remaining_shots * self.exposure

    @property 
    def remaining_shots(self):
        return self.count - self.finished

    @property
    def next_index(self):
        return self.finished + self.start_index

    @property
    def last_index(self):
        return self.next_index - 1

    def __str__(self):
        return 'Sequence {0}: {1} {2}s exposure (total exp time: {3}s)'.format(self.name, self.count, self.exposure,
                                                                               self.total_seconds)

    def __repr__(self):
        return self.__str__()
