import spacy
from spacy.symbols import ORTH, LEMMA

INPUT_STRING = 'I have flown to LA. Now I am flying to Frisco then will be driving to Salem.'

lemma_dict = {'fly', 'drive', 'bike'}
verb_type = {'VBG', 'VB'}

nlp = spacy.load('en') # Language Object
special_lemma = [{ORTH: 'Frisco', LEMMA: 'San Francisco'}]
nlp.tokenizer.add_special_case('Frisco', special_lemma)
doc = nlp(INPUT_STRING) # Doc Object
intent = []
# Loop through sentences
for sent in doc.sents:
    for word in sent:
        verb = word.head
        while verb.pos_ != 'VERB':
            if verb == verb.head:
                break
            verb = verb.head
        if verb.lemma_ in lemma_dict and verb.tag_ in verb_type:
            if word.ent_type != 0:
                intent.extend([verb.text, word.lemma_])

print(intent)

