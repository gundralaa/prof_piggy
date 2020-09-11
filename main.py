'''
Main monologue handling class
that generates the internal monologue
and calls the output handler to analyze ouput action
of each monologue line print 
'''
from inputs.text_input import TextInput
from outputs.output_handler import OutputHandler
from generator.model import GeneratorModel
import threading
from time import sleep
import numpy as np

class Monologue:
    inputs = ['text']
    # initializer
    def __init__(self):
        self.stop = [ False ]
        self.mono_lock = threading.Lock()
        self.actions = []
        self.in_obj = []
        self.mono_generator = self.init_generator()
        self.mono_list = []
        self.out_handler = OutputHandler(self.actions, self.mono_lock, self.stop)
        for input in self.inputs:
            if input == 'text':
                t = TextInput(self.mono_list, self.mono_lock, self.actions, self.stop)
                self.in_obj.append(t)
    # run method
    def run(self):
        out_thread = threading.Thread(target=self.out_handler.run, args=())
        out_thread.start()
        for machine_input in self.in_obj:
            thread = threading.Thread(target=machine_input.run, args=())
            thread.start()
        while not self.stop[0]:
            self.gen_mono()
            sleep(3)
            self.print_mono()
    # generate monologue
    def gen_mono(self):
        self.mono_lock.acquire()
        line = ''
        if len(self.mono_list) > 0:
            line = self.mono_generator.generate_line(self.mono_list[-1], 0.4)
        else:
            line = self.mono_generator.generate_line("I'm hungry", 0.4)
        self.mono_list.append(line)    
        # analyze generated monologue for action and add
        # self.actions.append()
        self.mono_lock.release()
    # print monologue
    def print_mono(self):
        self.mono_lock.acquire()
        with open('mono.out', 'a') as mono_file:
            mono_file.write(self.mono_list.pop() + '\n')
        # print('Added to File')
        self.mono_lock.release()
    # create a generator model
    def init_generator(self):
        text = ''
        with open('generator/wattpad.txt', 'rb') as wattpad:
            text = wattpad.read().decode(encoding='ascii')
        vocab = sorted(set(text))
        char_indx = {c:i for i, c in enumerate(vocab)}
        indx_char = np.array(vocab)
        generator = GeneratorModel(len(vocab), char_indx, indx_char, './generator/training_checkpoints')
        return generator

if __name__ == "__main__":
    open('mono.out', 'w').close()
    mono = Monologue()
    mono.run()


        
        
        
        


