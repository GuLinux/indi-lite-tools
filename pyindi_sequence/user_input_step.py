import sys

class UserInputStep:
    DEFAULT_PROMPT = 'Press Enter to continue'
    # the on_input callback, if specified, will be called with the user entered input
    def __init__(self, prompt = DEFAULT_PROMPT, on_input = None):
        self.prompt = prompt
        self.on_input = on_input

    def run(self):
        user_input = None
        if sys.version_info[0] < 3:
            user_input = raw_input(self.prompt)
        else:
            user_input = input(self.prompt)
        if self.on_input:
            self.on_input(user_input)
    
    def __str__(self):
        return 'Wait for user confirmation'

    def __repr__(self):
        return self.__str__()

 
