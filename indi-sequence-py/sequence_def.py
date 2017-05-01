from sequence_runner import SequenceRunner 
from sequence import Sequence
from auto_dark import *

class CameraMock:
    def set_exposure(self, exp):
        print('Setting exposure: {0}'.format(exp))

    def shoot(self):
        print('Shooting: {0}'.format(self.output))

    def set_output(self, out):
        self.output = out

camera = CameraMock()
auto_dark_calculator = AutoDarkCalculator()

def new_sequence(name, exposure, count):
    return Sequence(camera, name, exposure=exposure, count=count, on_finished=auto_dark_calculator.sequence_finished)

sequence_def = {
    'sequences': [
        new_sequence('Light', 10.2, 5),
        new_sequence('Light', 4, 5),
        new_sequence('Red', 6, 3),
        new_sequence('Green', 4, 3),
        new_sequence('Blue', 3, 3),
        AutoDarkSequence(camera, auto_dark_calculator) 
    ]
}

sequence_runner = SequenceRunner(None, sequence_def)

sequence_runner.start()

