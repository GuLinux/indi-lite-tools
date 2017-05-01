import os
class Session:
    def __init__(self, name, parent_directory):
        self.name = name
        self.path = os.path.join(parent_directory, name)
        self.sequence_groups = []
        self.camera = None

    def remove(self):
        # TODO: remove from filesystem
        pass

    def to_map(self):
        return {
                'name': self.name,
                'path': self.path,
                'sequence_groups': [x.to_map() for x in self.sequence_groups]
                }


