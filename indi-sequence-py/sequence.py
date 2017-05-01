import os

class SequenceCallbacks:
    def __init__(self, **kwargs):
        self.callbacks = kwargs

    def add(self, name, function):
        if not name in self.callbacks:
            self.callbacks[name] = []
        self.callbacks[name].append(function)

    def run(self, name, *args, **kwargs):
        if not name in self.callbacks:
            return
        for callback in self.callbacks[name]:
            callback(*args, **kwargs)

class Sequence:
    def __init__(self, camera, name, exposure, count, upload_path, **kwargs):
        self.camera = camera
        self.name = name
        self.count = count
        self.exposure = exposure
        self.upload_path = upload_path
        self.callbacks = SequenceCallbacks(**kwargs)
        self.finished = 0
        if not os.path.isdir(upload_path):
            os.makedirs(upload_path)

    def run(self):
        self.camera.set_upload_to('local')
        self.camera.set_upload_path(self.upload_path, '{0}_{1}s_XXX'.format(self.name, self.exposure))
        self.callbacks.run('on_started', self)

        for sequence in range(0, self.count):
            self.callbacks.run('on_each_started', self, sequence)
            self.camera.shoot(self.exposure)
            self.finished+=1
            self.callbacks.run('on_each_finished', self, sequence)


        self.callbacks.run('on_finished', self)

    def total_seconds(self):
        return self.exposure * self.count

    def shot_seconds(self):
        return self.finished * self.exposure

    def remaining_seconds(self):
        return (self.count - self.finished) * self.exposure

    def __str__(self):
        return 'Sequence {0}: {1} {2}s exposure (total exp time: {3}s)'.format(self.name, self.count, self.exposure, self.total_seconds())

    def __repr__(self):
        return self.__str__()
