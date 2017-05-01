class Sequence:
    def __init__(self, camera, name, exposure, count, on_started = None, on_finished = None, on_each_started = None, on_each_finished = None):
        self.camera = camera
        self.name = name
        self.count = count
        self.exposure = exposure
        self.on_started = self.__get_callbacks(on_started)
        self.on_finished = self.__get_callbacks(on_finished)
        self.on_each_started = self.__get_callbacks(on_each_started)
        self.on_each_finished = self.__get_callbacks(on_each_finished)
        self.finished = 0

    def run(self):
        self.camera.set_exposure(self.exposure)
        self.camera.set_output('{0}_{1}'.format(self.name, self.exposure))
        for on_started in self.on_started:
            self.on_started(self)

        for sequence in range(0, self.count):
            for on_each_started in self.on_each_started:
                on_each_started(self, sequence)
            self.camera.shoot()
            for on_each_finished in self.on_each_finished:
                on_each_finished(self, sequence)

        for on_finished in self.on_finished:
            on_finished(self)
        self.finished+=1

    def total_seconds():
        return self.exposure * self.count

    def shot_seconds():
        return self.finished * self.exposure

    def remaining_seconds():
        return (self.count - self.finished) * self.exposure

    def __get_callbacks(self, value):
        if not value:
            return []
        if hasattr(value, '__iter__'):
            return list(value)
        return [value]

