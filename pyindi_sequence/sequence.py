import os, time
from astropy.io import fits
import threading
import shutil
import functools
import tempfile

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

    def __init__(self, camera, exposure, count, upload_path, start_index=1, name=None, filename_template='{name}_{exposure}s_{number:04}.fits', **kwargs):
        self.camera = camera
        self.count = count
        self.exposure = exposure
        self.upload_path = upload_path
        self.callbacks = SequenceCallbacks(**kwargs)
        self.finished = 0
        self.start_index = start_index
        self.name = name
        self.filename_template = filename_template
        if not os.path.isdir(upload_path):
            os.makedirs(upload_path)
        self.max_threads = 2
        if 'MAX_INDI_MOVE_THREADS' in os.environ:
            self.max_threads = int(os.environ['MAX_INDI_MOVE_THREADS'])
        self.async_move_threads = [None] * self.max_threads
        self.__next_index = 0

    def run(self):
        self.camera.set_upload_to('local')
        tmp_prefix = self.name + 'TMP'
        tmp_upload_path = tempfile.gettempdir()
        tmp_file = os.path.join(tmp_upload_path, tmp_prefix + '.fits')


        self.camera.set_upload_path(tmp_upload_path, tmp_prefix)
        self.callbacks.run('on_started', self)

        for sequence in range(0, self.count):
            self.callbacks.run('on_each_started', self, sequence)
            # Check for 'pause' file
            while os.path.isfile(os.path.join(self.upload_path, 'pause')):
                time.sleep(0.5)

            temp_before = self.ccd_temperature
            self.camera.shoot(self.exposure)
            temp_after = self.ccd_temperature

            file_name = os.path.join(self.upload_path, self.filename_template.format(name=self.name, exposure=self.exposure, number=sequence + self.start_index))

            temperature = None
            if temp_before is not None and temp_after is not None:
                temperature = (temp_before + temp_after) / 2

            self.__start_thread_move(tmp_file, file_name, temperature)
            self.finished += 1
            self.callbacks.run('on_each_finished', self, sequence, file_name)

        self.callbacks.run('on_finished', self)

    def __start_thread_move(self, tmp_file, file_name, temperature):
        if self.max_threads == 0:
            self.__move_tmp_file(tmp_file, file_name, temperature)
        else:
            async_move_thread = threading.Thread(target=functools.partial(Sequence.__move_tmp_file, self, tmp_file, file_name, temperature))
            async_move_thread.start()
            if self.async_move_threads[self.__next_index]:
                self.async_move_threads[self.__next_index].join()
            self.async_move_threads[self.__next_index] = async_move_thread
            self.__next_index = (self.__next_index + 1) % self.max_threads

    def __move_tmp_file(self, temp_file, dest_file, temperature=None):
        # If temp_file and dest_file are on different filesystems (like /tmp and $HOME), the move will take some time, potentially clashing with the next capture.
        temp_unique_file = os.path.join(os.path.dirname(temp_file), os.path.basename(dest_file))
        # First, do a "fast" rename within the same filesystem, in order to free the temporary global file
        shutil.move(temp_file, temp_unique_file)
        
        # Write the average CCD temperature, if not present
        if temperature is not None:
            with fits.open(temp_unique_file, mode='append') as fits_file:
                if 'CCD-TEMP' not in fits_file[0].header:
                    fits_file[0].header['CCD-TEMP'] = (temperature, 'CCD Temperature (Celsius)')
                    fits_file.writeto(temp_unique_file, overwrite=True)


        # Then run the slower cross-fs move (cp + rm)
        shutil.move(temp_unique_file, dest_file)


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
        return 'Sequence {0}: {1} {2}s exposure (total exp time: {3}s), start index: {4}'.format(self.name, self.count,
                                                                                                 self.exposure,
                                                                                                 self.total_seconds,
                                                                                                 self.start_index)

    def __repr__(self):
        return self.__str__()
