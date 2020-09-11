'''
Input Class that runs seperate thread as main
and analyzes the input to generate a monologue
sentence
'''
from inputs.input import MachineInput
import spacy
import threading

class TextInput(MachineInput):
    # Todo handle am, is, are
    user_name = 'User'
    pron_you = {'you': 'i', 'your': 'my', 'yours': 'mine', 'yourself': 'myself'}
    pron_i = {'i': 'they', 'my': 'their', 'mine': 'theirs', 'am': 'are', 'are': 'am'}
    # initializer
    def __init__(self, mono_list, mono_lock, actions, stop):
        self.user_in = {}
        self.mono_out = ''
        self.stop = stop
        self.mono_list = mono_list
        self.actions = actions
        self.nlp = spacy.load('en')
        self.mono_lock = mono_lock
    # run method
    def run(self):
        while not self.stop[0]:
            text = input('Enter a sentence:\n').lower()
            if text == 'sleep':
                self.stop[0] = True
                return
            self.user_in = self.match_pattern(text)
            self.mono_out = self.gen_mono(self.user_in)
            self.post()
            print(self.mono_out)
    # run method for testing
    def run_test(self, text):
        self.user_in = self.match_pattern(text)
        self.mono_out = self.gen_mono(self.user_in)
        print(self.mono_out)
    # post method
    def post(self):
        self.mono_lock.acquire()
        self.mono_list.append(self.mono_out)
        self.actions.append(self.user_in)
        self.mono_lock.release()
    # finds the matched pattern and key tokens
    def match_pattern(self, text):
        doc = self.nlp(text)
        match, result = False, {}
        for fn in self.matchers():
            match, result = fn(doc)
            if match:
                return result
        return self.statement(text)
    # generate a monologue phrase as input
    def gen_mono(self, result):
        phrase = self.pron_switch(result['phrase'])
        vb = self.pron_switch(result['vb'])
        if result['type'] == 'statement':
            return self.user_name + ' said that ' + phrase
        if result['type'] == 'question':
            return self.user_name + ' asked me ' + phrase + vb
        if result['type'] == 'intent':
            return self.user_name + ' wants me to ' + vb + phrase

    '''
    Pattern matcher functions
    iterate through token body
    find relevant tokens
    format
    result = {'vb': '', 'obj': '', 'phrase': '', 'type': ''}
    '''
    # match intent verb 'intent' phrase
    def verb_intent(self, doc):
        result = {}
        for i, token in enumerate(doc):
            if token.dep_ == 'nsubj' and token.text == 'i':
                return False, result
            if token.dep_ == 'dobj':
                result = {
                    'vb': token.head.text,
                    'obj': token.text, 
                    'phrase': " ".join([w.text for w in doc]),
                    'type' : 'intent'
                }
                return True, result
        return False, result
    # match question intent
    def question(self, doc):
        result = {}
        bank = ['who', 'what', 'when', 'where', 'why', 'how']
        for i, token in enumerate(doc):
            if token.text in bank:
                phrase = ''
                vb = ''
                for j in range(i, len(doc)):
                    if doc[j].dep_ == 'ROOT':
                        vb = doc[j].text
                    else:
                        phrase = phrase + doc[j].text + ' '
                result = {
                    'vb': vb,
                    'obj': '', 
                    'phrase': phrase,
                    'type' : 'question'
                }
                return True, result
        return False, result
    # default result
    def statement(self, text):
        result = {
            'vb': '',
            'obj': '', 
            'phrase': text,
            'type' : 'statement'
        }
        return result
    # pronoun switcher
    def pron_switch(self, text):
        doc = self.nlp(text, disable=['parser', 'tagger', 'ner'])
        sent = ''
        for token in doc:
            if token.text in self.pron_you:
                sent = sent + self.pron_you[token.text] + ' '
            elif token.text in self.pron_i:
                sent = sent + self.pron_i[token.text] + ' '
            else:
                sent = sent + token.text + ' '
        return sent

    # returns a list of pattern matchers
    def matchers(self):
        return [self.verb_intent, self.question]


    

