'''
Scraper script to currently
compile a dataset of wattpad
first person stories for the
monologue generator training
'''

from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup
import spacy

# list of book ids
# id_list = [488498146, 494719170, 109534584, 94559190, 648657267, 439364087, 434903065]
id_list = [488498146]
open('wattpad.txt', 'w').close()
nlp = spacy.load('en', disable=["tagger", "parser"])

# entitiy recognizer
def entity_replace(text):
    doc = nlp(text)
    final = ""
    last_ind = 0
    for ent in doc.ents:
        if ent.label == 380:
            final += doc[last_ind : ent.start].text + ' User '
            last_ind = ent.end

    final += doc[last_ind:].text
    return final 

# loop through all books
for id in id_list:
    info = requests.get('https://www.wattpad.com/apiv2/info?id=' + str(id), headers={'User-Agent': 'Mozilla/5.0'})
    chapters = info.json()['group']
    # look through book chapters
    for chapter in chapters:
        chapter_id = str(chapter['ID'])
        story = Request('https://www.wattpad.com/apiv2/storytext?id=' + chapter_id, headers={'User-Agent': 'Mozilla/5.0'})
        text = urlopen(story).read()
        # format
        psoup = BeautifulSoup(text, features="html.parser")
        content = psoup.get_text()
        # replace person entities
        content = entity_replace(content)
        with open('wattpad.txt', 'a') as text_file:
            text_file.write("{}".format(content.encode('ascii', 'ignore')))

