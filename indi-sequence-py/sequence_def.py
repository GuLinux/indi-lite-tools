from sequence_runner import SequenceRunner 
from sequence import Sequence

class CameraMock:
    def set_exposure(self, exp):
        print('Setting exposure: {0}'.format(exp))

    def shoot(self):
        print('Shooting: {0}'.format(self.output))

    def set_output(self, out):
        self.output = out

camera = CameraMock()


sequence_def = {
    'sequences': [
        Sequence(camera, "Light", exposure=10.2, count=5),
        Sequence(camera, "Light", exposure=3, count=3),
        Sequence(camera, "Red", exposure=5, count=3),
        Sequence(camera, "Green", exposure=5, count=3),
        Sequence(camera, "Blue", exposure=5, count=3)
    ]
}

sequence_runner = SequenceRunner(None, sequence_def)

sequence_runner.start()

