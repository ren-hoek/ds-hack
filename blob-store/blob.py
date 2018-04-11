from azure.storage.blob import BlockBlobService
import pymongo as py
import os


def create_file_metadata(f, c):
    """Produce file metadata.

    Convert blob store file to metadata dictionary
    Input:
        f: blob filename
        c: container name
    Output:
        d: metadata dictionary
    """
    folder, filename = f.split('/')
    name, filetype = filename.split('.')
    cn, ty, dt = name.split('_')
    d = {
            'azure_folder': folder, 'filename': filename, 'name': name,
            'filetype': filetype, 'company_number': cn, 'doctype':ty,
            'submit_date': dt, 'blob_file': f, 'container': c
        }
    return d


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


def main():
    client = py.MongoClient(os.environ['MONGO_URI'])
    db = client.ch
    docs = db.docs

    included_folders = [
        'administratorsprogress',
        'companieshouseapi',
        'liquidatorsstatement'
        ]

    ch = AzureBlob(os.environ['BLOB_NAME'], os.environ['BLOB_KEY'])

    for container in ch.containers:
        if container.name in included_folders:
            for fl in ch.container_files(container):
                docs.insert_one(create_file_metadata(fl.name, container.name))


if __name__ == "__main__":
    main()

