'''
A question asking bot that loops through a statement
made by a user and generates a valid question using the sentence structure
of the sentence
Yes No
Uses inversion with subject and aux verb
Info
Uses a question word followed by statement
'''

import spacy
import sys

pron_convert = {
    'I' : 'you',
    'me' : 'you',
    'my' : 'your',
    'mine' : 'yours',
    'your' : 'my',
    'yours' : 'mine',
    'you' : 'I',
}

nlp = spacy.load('en')
# Returns the direct object noun chunk
def find_chunk(doc):
    chunk = ''
    for i, w in enumerate(doc):
        if w.dep_ == 'dobj':
            shift = len([a for a in w.children])
            chunk = doc[i-shift:i+1]
            break
    return chunk
# true for info and false for yes no question
def question_type(chunk):
    return any([w.dep_ == 'amod' for w in chunk])
# generate a question from a type and doc
def generate_question(doc, question_type):
    doc = invert(doc)
    doc = switch_pron(doc)
    if question_type:
        doc = 'Why ' + doc.text
    else:
        doc = doc[0].text.capitalize() + ' ' + doc[1:].text
    return doc
# invert the aux and pronoun
def invert(doc):
    sent = doc.text
    for i, w in enumerate(doc):
        # add do
        if w.tag_ == 'PRP' and doc[i+1].tag_ == 'VBP':
            sent = 'do ' + doc[i:].text
            break
        elif w.tag_ == 'PRP' and doc[i+1].tag_ == 'MD':
            sent = doc[i+1].text + ' ' + doc[i].text + ' ' + doc[i+2:].text
            break
    return nlp(sent)
# change pronouns
def switch_pron(doc):
    sent = ''
    for i, w in enumerate(doc):
        if w.text in pron_convert:
            sent = sent + pron_convert[w.text] + ' '
        elif w.text != '.':
            sent = sent + w.text + ' '
        else:
            sent = sent + '?'
    return nlp(sent)

#Main
#TEXT = 'I want a big orange.'
#doc = nlp(TEXT)
text = ''
while(True):
    text = input('Enter a sentence:\n')
    if (text == 'quit'):
        break
    doc = nlp(text)
    q_type = question_type(find_chunk(doc))
    print(generate_question(doc, q_type))