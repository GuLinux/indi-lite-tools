from sequence_runner import SequenceRunner 
from sequence import Sequence
from auto_dark import *
from camera import Camera
from indiclient import INDIClient 

indiclient = INDIClient()
camera = Camera('CCD Simulator', indiclient)
auto_dark_calculator = AutoDarkCalculator()
upload_path = '/home/marco/shots/M42'

def new_sequence(name, exposure, count):
    return Sequence(camera, name, exposure=exposure, count=count, upload_path=upload_path, on_finished=[auto_dark_calculator.sequence_finished])

sequence_def = {
    'sequences': [
        new_sequence('Light', 10.2, 5),
        new_sequence('Light', 4, 5),
        new_sequence('Red', 6, 3),
        new_sequence('Green', 4, 3),
        new_sequence('Blue', 3, 3),
        AutoDarkSequence(camera, auto_dark_calculator, upload_path) 
    ]
}

sequence_runner = SequenceRunner(None, sequence_def)

sequence_runner.start()

