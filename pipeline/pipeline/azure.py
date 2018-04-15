from azure.storage.blob import BlockBlobService
import pymongo as py
import os

class AzureBlob():
    """Wrapper around blob object.

    Return a blob object representing a blob storage
    container
    Inputs:
        con: A short name for a container
    """
    def __init__(self, con):
        if con == "ch":
            name = os.environ['BLOB_NAME']
            key = os.environ['BLOB_KEY']
        self.blob = BlockBlobService(
            account_name = name,
            account_key = key
        )
        self.containers = self.blob.list_containers()

    def container_files(self, c):
        return self.blob.list_blobs(c.name)


def remove_if_exists(f):
    """Remove file if exists.

    Remove a file but skips if file doesn't
    Inputs:
        f: path to file to remove
    Output:
        Boolean removed or not
    """
    try:
        os.remove(f)
        return True
    except OSError:
        pass
    return False


def get_cosmos_collection(s, d, c):
    """Get cosmosDB  collection.

    Returns a collection from a Cosmos MongoDB
    Inputs:
        s: Cosmos API
        d: Database name
        c: Collection name
    Output:
        t: Mongo collection
    """
    if s == 'mongo':
        client = py.MongoClient(os.environ['MONGO_URI'])
        db = client[d]
        t = db[c]
    return t


def update_cosmos_document(s, c, f, d):
    """Add field to cosmos document.

    Updates the cosmos record with processed field.
    Inputs:
        s: Cosmos API
        c: Mongo collection
        f: Cosmos document to update record
        d: Dictionary containing new field
    """
    for fl in c.find({'filename': f['filename']}):
        c.update_one({'_id': f['_id']}, {'$set': d})
    return True


def print_cosmos_document(s, c, f):
    """Add field to cosmos document.

    Updates the cosmos record with processed field.
    Inputs:
        s: Cosmos API
        c: Database name
        f: Cosmos document to update record
    """
    for fl in c.find({'filename': f['filename']}):
        print(fl)
    return True
