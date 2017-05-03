class RunFunctionStep:
    def __init__(self, function):
        self.function = function

    def run(self):
        self.function()
    
    def __str__(self):
        return 'Run python function'

    def __repr__(self):
        return self.__str__()

 
