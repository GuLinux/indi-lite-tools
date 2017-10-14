import subprocess


class ShellCommandStep:
    def __init__(self, arguments, shell=False, abort_on_failure=False):
        self.arguments = arguments
        self.shell = shell
        self.abort_on_failure = abort_on_failure

    def run(self):
        print('Running shell command {0}'.format(self.arguments))
        exit_code = subprocess.call(self.arguments, shell = self.shell)
        message = 'Shell command exited with status {0}'.format(exit_code)
        if exit_code != 0 and self.abort_on_failure:
            raise RuntimeError(message)
        else:
            print(message)
    
    def __str__(self):
        return 'Run shell command {0}'.format(self.arguments)

    def __repr__(self):
        return self.__str__()

 
