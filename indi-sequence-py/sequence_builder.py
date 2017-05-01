from sequence_runner import SequenceRunner 
from sequence import Sequence
from auto_dark import *
from camera import Camera
from indiclient import INDIClient 
import os
import time


class SequenceBuilder:
    def __init__(self, name, camera_name = None, upload_path = None, indi_host = INDIClient.DEFAULT_HOST, indi_port = INDIClient.DEFAULT_PORT):
        self.sequences = []
        self.name = name
        self.indi_client = INDIClient(indi_host, indi_port)
        self.auto_dark_calculator = AutoDarkCalculator()
        self.set_camera(camera_name)

        if not upload_path:
            upload_path = os.path.join(os.environ['HOME'], 'Shots', name)
        print('Will save fits file into {0}'.format(upload_path))
        self.upload_path = upload_path

    def devices(self):
        return self.indi_client.listDeviceNames()

    def set_camera(self, camera_name):
        if not camera_name:
            time.sleep(1)
            print('Camera name cannot be empty. Available devices: {0}'.format(', '.join(self.devices())))
            self.camera = None
            return
        self.camera = Camera(camera_name, self.indi_client)

    def add_sequence(self, sequence_name, exposure, count):
        self.sequences.append(Sequence(self.camera, sequence_name, exposure=exposure, count=count, upload_path=self.upload_path, on_finished=[self.auto_dark_calculator.sequence_finished]))
        return self

    def add_auto_datk(self, count = 10):
        self.sequences.append(AutoDarkSequence(self.camera, self.auto_dark_calculator, self.upload_path, count)) 
        return self

    def start(self):
        sequence_def = {
            'sequences': self.sequences
        }
        sequence_runner = SequenceRunner(sequence_def)
        sequence_runner.start()

    def help(self):
        print('\n'.join(['constructor: SequenceRunner(name, [camera_name, upload_path, indi_host, indi_port).',
               'devices(): returns a list of INDI device names.',
               'set_camera(camera_name): sets default camera to "camera_name".',
               'add_sequence(sequence_name, exposure, count): adds a sequence with <count> exposures of <exposure> seconds.',
               'add_auto_dark(<count = 10>): adds a sequence shooting dark frames for all exposures captured until now, <count> dark frames for each exposure.',
               'start(): starts capturing']))

    def __str__(self):
        to_s = [
            'SequenceBuilder object "{0}"'.format(self.name),
            'upload path: {0}'.format(self.upload_path),
            self.camera if self.camera else 'Camera not set',
            self.indi_client
        ]
        to_s.extend(self.sequences)
        return '\n'.join([str(s) for s in to_s])

    def __repr__(self):
        return self.__str__()
