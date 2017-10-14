import itertools

class SequenceRunner:
    def __init__(self, sequence_def):
        self.sequence_def = sequence_def

    def start(self):
        total_seconds = sum([s.total_seconds for s in self.sequence_def['sequences'] if hasattr(s, 'total_seconds')])

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
        print('++++ Sequence {0} started: exposure time: {1}s'.format(sequence.name, sequence.total_seconds))

    def __log_sequence_finished(self, sequence):
        print('++++ Sequence {0} finished: exposure time: {1}s'.format(sequence.name, sequence.total_seconds))

    def __log_sequence_each_finished(self, sequence, number, file_name):
        print('****** Sequence {0}: {1} of {2} finished, elapsed: {3}s, remaining: {4}s (total: {5}s)'.format(
            sequence.name, number+1, sequence.count, sequence.shot_seconds, sequence.remaining_seconds, sequence.total_seconds
        ))
