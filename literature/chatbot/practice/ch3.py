# Spacy Basic Container Objects
import spacy

nlp = spacy.load('en')
# doc object
doc = nlp('I wrote a large fake test sentence.')
print([doc[i] for i in range(len(doc))]) # indexable
# iterating over syntatcic children
last = doc[len(doc) - 2] # skip period for last word
print([w.text for w in last.lefts]) # left children iterate
print([w.text for w in last.children]) # all children
# verb iteration
verb = doc[1]
print([w.text for w in verb.rights]) # right children
# sents or sentences
doc = nlp('I wrote a large fake test sentence. There is now another sentence.')
for sent in doc.sents:
    print([sent[i] for i in range(len(sent))])
# noun chunks
for chunk in doc.noun_chunks:
    print(chunk) # the sytactic children of nouns and noun
# span
span = doc[5:7] # allows to group words together
span.merge()
print([w.text for w in doc])
'''
Custom Pipeline System
'''
print(nlp.pipe_names)
# a pipe has a part of speech tagger 'tagger'
# a dependency paser 'parser'
# an entity recognizer 'ner' (proper nouns)
nlp = spacy.load('en', disable=['parser']) # Disable parts of the pipe
doc = nlp('This has no dependency.')
print(doc[1].text, doc[1].dep_) # empty dep_
# Can edit parts of a pipeline and train them
# Cython Linking?








