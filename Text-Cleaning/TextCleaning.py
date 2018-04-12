import spacy
import pymongo as py
import sys
import requests
import json
import re
from geojson import Point, Feature, FeatureCollection
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
    out_dict['tokens'] = [ t.lemma_ for t in doc if not (t.is_stop or t.pos_ in ["PUNCT", "SPACE", "NUM"] or t.text == "\ufeff") ]

    #populate the named entity slots first removing any entities that are just whitespace
    doc.ents = [e for e in doc.ents if not e.text.isspace()]
    for ent in doc.ents:
        out_dict['Named Entity - '+ ent.label_].append(ent.text.strip())

    return out_dict 


def geocode(pcodes):

    """Geocodes a list of postcodes to produce a MultiPoint geojson object"""
    
    headers = {"Content-Type": "application/json"}
    url = "https://api.postcodes.io/postcodes?filter=postcode,longitude,latitude"

    pc_data = { 'postcodes' : list(set(pcodes)) }

    response = requests.post(url, data=json.dumps(pc_data), headers=headers)
    resp_obj = json.loads(response.text)


    #for a featurecollection - would be ideal but not sure it works well with mongo
    """fc = []

    for r in [ ro['result'] for ro in resp_obj['result']]:
        p = Point((r['longitude'], r['latitude']))
        f = Feature(geometry=p, properties={"postcode": r['postcode']})
        fc.append(f)

    features = FeatureCollection(fc)
    """

    #for a multipoint
    ps = [ (ro['result']['longitude'],ro['result']['latitude']) for ro in resp_obj['result']]

    mp = MultiPoint(ps)

    #print(mp)
    
    return mp



def main():
    """Requires the mongodb connection string as an arguement"""

    postcode_regex = "([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9]?[A-Za-z]))))\s?[0-9][A-Za-z]{2})"
    p = re.compile(postcode_regex)

    for f in p.finditer(accounts_txt):
        print(f.group(0))

    pcodes = [f.group(0) for f in p.finditer(accounts_txt)]

    mp = geocoder(pcodes)

    
    #Read in the connection string from the command line
    MONGO_URI = sys.argv[1]
    
    #initialise resources
    spacy.load('en')
    client = py.MongoClient(MONGO_URI)
    db = client.ch
    
    #get the documents with text added
    fs = db.docs.find(
                {
                    'filetype': 'pdf',
                    'doctype': 'annual-returns',
                    'extracted_hand': {'$exists': True}
                }
            )
    
    for i, f in enumerate(fs):
        #joins the returned text into a single string and cleans up
        f_txt = " ".join( f['extracted_hand'] )
        out_dict = text_cleaner(f_txt)
        
        #looks for postcodes and adds a multipoint to the dictionary if any are found
        pcodes = [f.group(0) for f in p.finditer(accounts_txt)]
        
        if len(pcodes) > 0: 
            mp = geocode(pcodes)
            out_dict['geometry'] = mp
        
        #update 
        db.docs.update_one({'_id': f['_id']}, {'$set': out_dict })
        
        
        
if __name__ == "__main__":
    main()


