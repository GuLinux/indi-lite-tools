import itertools

class SequenceRunner:
    def __init__(self, sequence_def):
        self.sequence_def = sequence_def

    def start(self):
        total_seconds = reduce( lambda acc, seq: acc + seq.total_seconds() if hasattr(seq, 'total_seconds') else acc, self.sequence_def['sequences'], 0)
        print('== Starting sequences: total exposure time={0} seconds'.format(total_seconds))
        for sequence in self.sequence_def['sequences']:
            self.__run_sequence(sequence)

    def __run_sequence(self, sequence):
        if hasattr(sequence, 'callbacks'):
            sequence.callbacks.add('on_started', self.__log_sequence_started)
            sequence.callbacks.add('on_finished', self.__log_sequence_finished)
            sequence.callbacks.add('on_each_finished', self.__log_sequence_each_finished)
        sequence.run()

    def __log_sequence_started(self, sequence):
        print('++++ Sequence {0} started: exposure time: {1}'.format(sequence.name, sequence.total_seconds()))

    def __log_sequence_finished(self, sequence):
        print('++++ Sequence {0} finished: exposure time: {1}'.format(sequence.name, sequence.total_seconds()))

    def __log_sequence_each_finished(self, sequence, number):
        print('****** Sequence {0}: {1} of {2} finished, elapsed: {3}, remaining: {4} (total: {5})'.format(
            sequence.name, number+1, sequence.count, sequence.shot_seconds(), sequence.remaining_seconds(), sequence.total_seconds()
        ))
