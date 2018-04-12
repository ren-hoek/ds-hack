import os
import pymongo as py

def main():
    client = py.MongoClient(os.environ['MONGO_URI'])
    db = client.ch
    print(db.docs.aggregate([{"$group": {"_id": "$filetype", "count": {"$sum": 1}}}]))

if __name__ == "__main__":
    main()
