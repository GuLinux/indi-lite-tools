import time
from device import Device
import PyIndi


class Camera(Device):
    def __init__(self, name, indi_client, connect_on_create = True):
        Device.__init__(self, name, indi_client)
        if connect_on_create:
            self.connect()

    def shoot(self, exposure):
        self.set_number('CCD_EXPOSURE', {'CCD_EXPOSURE_VALUE': exposure})

    def set_upload_path(self, path, prefix = 'IMAGE_XXX'):
        self.set_text('UPLOAD_SETTINGS', {'UPLOAD_DIR': path, 'UPLOAD_PREFIX': prefix})

    def set_upload_to(self, upload_to = 'local'):
        upload_to = {'local': 'UPLOAD_LOCAL', 'client': 'UPLOAD_CLIENT', 'both': 'UPLOAD_BOTH'}[upload_to]
        self.set_switch('UPLOAD_MODE', [upload_to] )


