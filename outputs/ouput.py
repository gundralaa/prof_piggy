'''
Basic abstract class that defines an
output class from the many output classes
'''
class MachineOutput():
    # run method that performs the output piece
    def run(self):
        pass
    # post method changes any states
    def post(self):
        pass