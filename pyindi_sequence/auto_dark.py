from pyindi_sequence.sequence import Sequence, SequenceCallbacks

class AutoDarkCalculator:
    def __init__(self):
        self.reset()

    def sequence_finished(self, sequence):
        self.exposures.add(sequence.exposure)

    def reset(self):
        self.exposures = set()

class AutoDarkSequence:
    def __init__(self, camera, auto_dark_calculator, upload_path, count = 10, **kwargs):
        self.camera = camera
        self.auto_dark_calculator = auto_dark_calculator
        self.count = count
        self.upload_path = upload_path
        self.callbacks = SequenceCallbacks(**kwargs)

    def run(self):
        for exposure in self.auto_dark_calculator.exposures:
            sequence = Sequence(self.camera, "Dark", exposure, self.count, self.upload_path)
            sequence.callbacks = self.callbacks
            sequence.run()
        self.auto_dark_calculator.reset() 

    def __str__(self):
        return 'AutoDarkSequence (exposures: {0})'.format(', '.join(self.auto_dark_calculator.exposures))

    def __repr__(self):
        return self.__str__()
