from sequence import Sequence, SequenceCallbacks

class AutoDarkCalculator:
    def __init__(self):
        self.reset()

    def sequence_finished(self, sequence):
        self.exposures.add(sequence.exposure)

    def reset(self):
        self.exposures = set()

class AutoDarkSequence:
    def __init__(self, camera, auto_dark_calculator, count = 10, **kwargs):
        self.camera = camera
        self.auto_dark_calculator = auto_dark_calculator
        self.count = count
        self.callbacks = SequenceCallbacks(**kwargs)

    def run(self):
        for exposure in self.auto_dark_calculator.exposures:
            sequence = Sequence(self.camera, "Dark", exposure, self.count)
            sequence.callbacks = self.callbacks
            sequence.run()
        self.auto_dark_calculator.reset() 

