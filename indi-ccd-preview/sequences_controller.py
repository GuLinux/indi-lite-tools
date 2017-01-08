import glob
import shlex
import os

class Sequence:
    def __init__(self, file):
        self.file = file
        self.__parse()

    def to_map(self):
        return {'name': self.SESSION_NAME, 'pid': self.SESSION_PID, 'file': self.file}

    def is_active(self):
        return os.path.isdir('/proc/{0}'.format(self.SESSION_PID))

    def create_continue_file(self):
        path = self.file.split('.')[:-1]
        path.append('confirmation')
        open('.'.join(path), 'a').close()

    def __parse(self):
        with open(self.file, 'r') as f:
            lines = shlex.split(f.read())
            for line in lines:
                parsed = line.split('=')
                self.__dict__[parsed[0]] = parsed[1]
                
    
class SequencesController:

    SEQ_DIRECTORY = '/tmp/indi_sequence_script'
    def __init__(self):
        pass

    def sequences(self):
        sequences = []
        for file in glob.glob('{0}/*.info'.format(SequencesController.SEQ_DIRECTORY)):
            sequence = Sequence(file)
            if sequence.is_active():
                sequences.append(sequence)
        return sequences

    def continue_sequence(self, name):
        for sequence in self.sequences():
            if sequence.SESSION_NAME == name:
                sequence.create_continue_file()
