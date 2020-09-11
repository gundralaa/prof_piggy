'''
Text Output
The main print output handler
that prints directly to the terminal
of the computer or other target areas
May be combined with other output actions
Main function is to generate text according
to the output handler
'''
from outputs.ouput import MachineOutput

class TextOutput(MachineOutput):
    # initializer defines the direction of output
    def __init__(self, target):
        self.target = target
        self.content = ''
    # sets the content to be printed
    def set_content(self, content):
        # TODO might change to transform text with right pronouns
        self.content = content
    # run method prints based on target
    def run(self):
        if self.target == 'terminal':
            print(self.content)
        self.post()
    # post method to update action history
    def post(self):
        pass