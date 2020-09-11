'''
Intent Output Handler
Uses the result objects
that are formatted as a dictionary
such that
{
    'vb': verb with action
    'obj': the object of the verb
    'phrase' : the noun chunk representing the object
    'type' : the phrase type
        (could be intent, question, statement etc)
}
'''
import threading
from outputs.text_output import TextOutput
from outputs.alarm_output import AlarmOutput

class OutputHandler():
    outputs = ['text', 'alarm']
    # initializer
    def __init__(self, actions, mono_lock, stop):
        self.actions = actions
        self.mono_lock = mono_lock
        self.out_objs = {}
        self.stop = stop
        for output in self.outputs:
            if output == 'text':
                text_out = TextOutput('terminal')
                self.out_objs[output] = text_out
            elif output == 'alarm':
                alarm_out = AlarmOutput(self.out_objs['text'])
                self.out_objs[output] = alarm_out
    # run method that runs the handler
    def run(self):
        while not self.stop[0]:
            self.out_objs['alarm'].run()
            action = self.check_action()
            out_obj = self.decide_action(action)
            self.run_action(out_obj)
    # check for next action
    def check_action(self):
        # the action object
        action = ''
        if self.actions:
            self.mono_lock.acquire()
            action = self.actions.pop()
            self.mono_lock.release()
        return action
    # decide the action to take
    def decide_action(self, action):
        if action:
            if action['obj'] == 'alarm':
                self.out_objs['alarm'].add_event(action['phrase'])
            if action['type'] == 'intent':
                self.out_objs['text'].set_content(action)
                return self.out_objs['text']
            
        return ''
    # run the output selected
    def run_action(self, out):
        if out:
            out.run()
        


