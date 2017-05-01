class SequenceRunner:
    def __init__(self, indiclient, sequence_def):
        self.indiclient = indiclient
        self.sequence_def = sequence_def

    def start(self):
        for sequence in self.sequence_def['sequences']:
            self.__run_sequence(sequence)

    def __run_sequence(self, sequence):
        sequence.run()
