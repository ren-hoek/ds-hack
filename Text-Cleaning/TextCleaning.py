import spacy
from collections import defaultdict

spacy.load('en')

def text_cleaner(text):
    nlp = spacy.load('en', tagger=False, parser=False, matcher=False)
    doc = nlp(text)

    out_dict = defaultdict(list)

    out_dict['tokens'] = [t.lemma_ for t in doc if not (t.is_stop or t.pos_ == "PUNCT") ]

    for ent in doc.ents:
        out_dict['Named Entity - '+ ent.label_].append(ent.text)

    print(out_dict)

    return out_dict 
