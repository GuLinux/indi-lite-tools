class SequenceGroup:
    def __init__(self, name):
        self.name = name
        self.sequences = []

    def to_map(self):
        return {
                'name': self.name
                }
