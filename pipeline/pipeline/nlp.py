import spacy
from collections import defaultdict

def text_cleaner(text):
    """Lemmatizes tokens and removes stop words, punctuation, and numbers. Identifies named entities.
    Returns a dictionary of lists keyed on tokens and different types of named entities keyed in the form
    'Named Entity - ORG', see spacy docs for the list of entity types

    Arguments:
    text - raw text to tokenize may need to run re.sub(r'\n', ' ', text) to clean up

    """

    #load the text into spacy to tag
    nlp = spacy.load('en', tagger=False, parser=False, matcher=False)
    doc = nlp(text)

    #TODO - break up the text by page or paragraph using repeat newlines?

    #setup output as a default dictionary of lists
    out_dict = defaultdict(list)

    #populate the tokes slot removing spaces, numbers and punctuation etc.
    out_dict['tokens'] = [
            t.lemma_ for t in doc if not (
                t.is_stop or t.pos_ in ["PUNCT", "SPACE", "NUM"] or t.text == "\ufeff"
            )
        ]

    #populate the named entity slots first removing any entities that are just whitespace
    doc.ents = [e for e in doc.ents if not e.text.isspace()]
    for ent in doc.ents:
        out_dict['Named Entity - '+ ent.label_].append(ent.text.strip())

    return out_dict

