'''
When executed sets an alarm for a given time
during the day that resets everyday. When the
time comes to pass, the module with remind the 
user with the event specified.
'''

from outputs.ouput import MachineOutput
import os
import spacy
import time
import pync

class AlarmOutput(MachineOutput):
    # initializer
    def __init__(self, text_out):
        self.time_lst = {}
        self.nlp = spacy.load('en')
    # add event to list
    def add_event(self, phrase):
        hour, message = self.extract_time(phrase)
        if not hour or not message:
            return
        if hour in self.time_lst:
            self.time_lst[hour].append(message)
        else:
            self.time_lst[hour] = [message]
        pync.notify('Alarm set for ' + message + ' at ' + hour)
    # run method, checks current time and if time
    # in the hashmap
    def run(self):
        hour = time.localtime().tm_hour
        if hour in self.time_lst:
            for message in self.time_lst[hour]:
                pync.notify(message)
    # use nlp to extract the time and message
    def extract_time(self, phrase):
        doc = self.nlp(phrase)
        hour, message = '', ''
        for i, t in enumerate(doc):
            if t.pos_ == 'NUM':
                hour = t.text
            elif t.text == 'for':
                message = doc[i+1:].text
                break
        if not hour or not message:
            print('Could not set alarm, try again')
        return hour, message
