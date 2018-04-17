from azure.storage.blob import BlockBlobService
import pymongo as py
import os
import re
from bs4 import BeautifulSoup


_maxNumRetries = 10


def find(key, dictionary):
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result


class AzureBlob():
    """Wrapper around blob object."""
    def __init__(self, name, key):
        self.blob = BlockBlobService(
            account_name = name,
            account_key = key
        )
        self.containers = self.blob.list_containers()

    def container_files(self, c):
        return self.blob.list_blobs(c.name)


def extract_xhtml(xhtml):

    soup = BeautifulSoup(open(xhtml), 'html.parser')

    for tag in soup(["script", "style"]):
        tag.extract()

    text = re.sub('<[^<]+>', " ",str(soup))

    text = text.replace("\n", " ")
    text = re.sub(r'[\W_]+', ' ', text)
    text = text.split(" ")

    return text


def remove_if_exists(f):
    """Remove file if exists.

    Remove a file but skips if file doesn't
    Inputs:
        f: path to file to remove
    Output:
        Boolean removed of not
    """
    try:
        os.remove(f)
        return True
    except OSError:
        pass
    return False


def main():
    client = py.MongoClient('mongodb://cosmo-feynman:4rDaE4LwLhwtwKCRIID7BV42Dpz9JOcj3H8kTDUqDmDbkmJiW4HqcGmktibeGWdAkFE5ZE8bQPvR1EncGLSiGA==@cosmo-feynman.documents.azure.com:10255/?ssl=true&replicaSet=globaldb') #MONGO_URI
    db = client.ch

    ch = AzureBlob('hmrchackathon', 'E6AiDaSVSsj7SaQWBB32KwaR4rtIAxu0+Jz8aD/V8S1jJafINMJFYDVBOic8NZVotRmKvwpGNmtT/Vh0w47zGg==') # BLOB_NAME # BLOB_KEY

    blob_files = db.docs.find({'filetype': 'xhtml'})

    print(blob_files.count())

    for i, blob_file in enumerate(blob_files):
        try:
            ch.blob.get_blob_to_path(
                blob_file['container'],
                blob_file['blob_file'],
                blob_file['filename']
                )

            text_output = {'extract_html': str(extract_xhtml(blob_file['filename']))}


        except:
            text_output = {'extracted_xhmtl': ''}

        for f in db.docs.find({'filename': blob_file['filename']}):
            db.docs.update_one({'_id': f['_id']}, {'$set': text_output})

        for f in db.docs.find({'filename': blob_file['filename']}):
            print(f)

        remove_if_exists(blob_file['filename'])




if __name__ == "__main__":
    main()

