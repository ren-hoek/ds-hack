from pipeline import azure as az
from pipeline import ocr


def main():
    docs = az.get_cosmos_collection('mongo', 'ch', 'docs')
    ch = az.AzureBlob('ch')
    blob_file = docs.find_one({'filetype': 'pdf', 'doctype': 'annual-returns'})

    print(blob_file['container'], blob_file['blob_file'])

    ch.blob.get_blob_to_path(
            blob_file['container'],
            blob_file['blob_file'],
            blob_file['filename']
        )

    pages = ocr.create_jpg(blob_file['filename'])
    print(pages['page_count'])
    print(pages['pages'])

    az.remove_if_exists(blob_file['filename'])
    az.remove_if_exists('test.jpg')


if __name__ == "__main__":
    main()


"""
local_file  = '/home/gavin/Projects/ds-hack/blob-store/' + blob_files[0][1]
"""

