class Sequence:
    def __init__(self, camera, name, exposure, count):
        self.camera = camera
        self.name = name
        self.count = count
        self.exposure = exposure

    def run(self):
        self.camera.set_exposure(self.exposure)
        self.camera.set_output('{0}_{1}'.format(self.name, self.exposure))
        for sequence in range(0, self.count):
            self.camera.shoot()

