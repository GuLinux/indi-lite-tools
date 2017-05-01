import sys

class UserInputStep:
    DEFAULT_PROMPT = 'Press Enter to continue'
    def __init__(self, prompt = DEFAULT_PROMPT):
        self.prompt = prompt

    def run(self):
        if sys.version_info[0] < 3:
            raw_input(self.prompt)
        else:
            input(self.prompt)
    
    def __str__(self):
        return 'Wait for user confirmation'

    def __repr__(self):
        return self.__str__()

 
