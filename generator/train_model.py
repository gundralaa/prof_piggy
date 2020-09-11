'''
Script to properly filter through
wattpad input and train the textgen model
and save the model to weights file
'''
from model import GeneratorModel
import tensorflow as tf
import numpy as np
import os
import time

# data cleaning
# use a char based rnn due to high vocab size of word based
text = ''
with open('wattpad.txt', 'rb') as wattpad:
    text = wattpad.read().decode(encoding='ascii')
vocab = sorted(set(text))
# char to indx dict
char_indx = {c:i for i, c in enumerate(vocab)}
# idx back to char
indx_char = np.array(vocab)
print(char_indx)
# create text vec
text_indx = [char_indx[c] for c in text]

# train
generator = GeneratorModel(len(vocab), char_indx, indx_char, './training_checkpoints')
#generator.build(True)
#generator.train(text_indx, 2500)

# generate examples
for i in range(15):
  print(generator.generate_line('"I hate you" User said.', 0.6))


# initialize new base model
'''
textgen = textgenrnn()
textgen.train_from_file('wattpad.txt', num_epochs=10)
textgen.save('wattpad_gen_weights.hdf5')
'''
