'''
Text script that generates
monologue lines using the trained
model from wattpad
'''

from textgenrnn import textgenrnn

# initialize new model
textgen = textgenrnn('weights/wattpad_gen_weights.hdf5')
textgen.generate(5)