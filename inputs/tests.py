'''
Unit tests for inputs
'''

from inputs.text_input import TextInput

# Text Input
t_in = TextInput()
# question input
t_in.run_test('what is the best restaurant nearby')
# intent input
t_in.run_test('Adam, please write me a function in python because I am currently occupied')
# pronoun switch
t_in.run_test('Adam, take better care of yourself')
# statement input
t_in.run_test('you are fantastic')
# input test
t_in.run()
