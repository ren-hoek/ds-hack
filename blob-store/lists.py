import os
import pymongo as py

def main():
    client = py.MongoClient(os.environ['MONGO_URI'])
    db = client.ch

    print(set([x['filetype'] for x in db.docs.find()]))
    print(db.docs.find({'filetype': 'xhtml'}).count())
    print(
            db.docs.find(
                {
                    'filetype': 'pdf',
                    'doctype': 'annual-returns',
                    'extracted_hand': {'$exists': True}
                }
            ).count()
    )

if __name__ == "__main__":
    main()
