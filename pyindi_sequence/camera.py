import time
from pyindi_sequence.device import Device
import PyIndi

class CameraChangeSettingsStep:
    def __init__(self, camera, roi = None, binning = None, compression_format = None, frame_type = None, controls = None, numbers = None, switches = None):
        self.camera = camera
        self.roi = roi
        self.binning = binning
        self.compression_format = compression_format
        self.frame_type = frame_type
        self.controls = controls
        self.numbers = numbers
        self.switches = switches

    def run(self):
        if self.roi:
            self.camera.set_roi(self.roi)
        if self.binning:
            self.camera.set_binning(self.binning)
        if self.compression_format:
            self.camera.set_compression_format(self.compression_format)
        if self.frame_type:
            self.camera.set_frame_type(self.frame_type)
        if self.controls:
            self.camera.set_controls(self.controls)
        if self.numbers:
            for control_name, control_values in self.numbers.items():
                self.camera.set_number(control_name, control_values)
        if self.switches:
            for control_name, control_values in self.switches.items():
                self.camera.set_switch(control_name, control_values['on'] if 'on' in control_values else [], control_values['off'] if 'off' in control_values else [])

    def __str__(self):
        values = [['roi', self.roi], ['bin', self.binning], ['compression_format', self.compression_format], ['frame_type', self.frame_type], ['controls', self.controls], ['numbers', self.numbers], ['switches', self.switches]]
        values = [': '.join([x[0], str(x[1])]) for x in values if x[1]]
        return 'Change camera settings: {0}'.format(', '.join(values))

    def __repr__(self):
        return self.__str__()


class Camera(Device):
    def __init__(self, name, indi_client, connect_on_create = True):
        Device.__init__(self, name, indi_client)
        if connect_on_create:
            self.connect()

    def shoot(self, exposure):
        self.set_number('CCD_EXPOSURE', {'CCD_EXPOSURE_VALUE': exposure}, timeout=exposure * 1.5 + 20)

    def set_upload_path(self, path, prefix = 'IMAGE_XXX'):
        self.set_text('UPLOAD_SETTINGS', {'UPLOAD_DIR': path, 'UPLOAD_PREFIX': prefix})

    def binning(self):
        return self.values('CCD_BINNING', 'number')

    def set_binning(self, hbin, vbin = None):
        if vbin == None:
            vbin = hbin
        self.set_number('CCD_BINNING', {'HOR_BIN': hbin, 'VER_BIN': vbin })

    def set_roi(self, roi):
        self.set_number('CCD_FRAME', roi)

    def roi(self):
        return self.values('CCD_FRAME', 'number')

    def compression_format(self):
        return self.switch_values('CCD_COMPRESSION')

    def set_compression_format(self, ccd_compression):
        self.set_switch('CCD_COMPRESSION', [ccd_compression])

    def frame_type(self):
        return self.switch_values('CCD_FRAME_TYPE')

    def set_frame_type(self, frame_type):
        self.set_switch('CCD_FRAME_TYPE', [frame_type])

    def controls(self):
        return self.values('CCD_CONTROLS', 'number')

    def set_controls(self, controls):
        self.set_number('CCD_CONTROLS', controls)

    def set_upload_to(self, upload_to = 'local'):
        upload_to = {'local': 'UPLOAD_LOCAL', 'client': 'UPLOAD_CLIENT', 'both': 'UPLOAD_BOTH'}[upload_to]
        self.set_switch('UPLOAD_MODE', [upload_to] )

    def exposure_range(self):
        ctl = self.get_control('CCD_EXPOSURE', 'number')[0]
        return {
            'minimum': ctl.min,
            'maximum': ctl.max,
            'step': ctl.step
        }

    def __str__(self):
        return 'INDI Camera "{0}"'.format(self.name)

    def __repr__(self):
        return self.__str__()
