class SequenceRunner:
    def __init__(self, indiclient, sequence_def):
        self.indiclient = indiclient
        self.sequence_def = sequence_def

    def start(self):
        for sequence in self.sequence_def['sequences']:
            self.__run_sequence(sequence)

    def __run_sequence(self, sequence):
        sequence.callbacks.add('on_started', self.__log_sequence_started)
        sequence.callbacks.add('on_finished', self.__log_sequence_finished)
        sequence.run()

    def __log_sequence_started(self, sequence):
        print('Sequence {0} started: exposure time: {1}'.format(sequence.name, sequence.total_seconds()))

    def __log_sequence_finished(self, sequence):
        print('Sequence {0} finished: exposure time: {1}'.format(sequence.name, sequence.total_seconds()))
