from pipeline import azure as az
from pipeline import xhtml as xh


def main():
    docs = az.get_cosmos_collection('mongo', 'ch', 'docs')
    ch = az.AzureBlob('ch')
    blob_files = docs.find({'filetype': 'xhtml'})


    for i, blob_file in enumerate(blob_files):
        if i>4:
            break
        print(blob_file['container'], blob_file['blob_file'])
        ch.blob.get_blob_to_path(
            blob_file['container'],
            blob_file['blob_file'],
            blob_file['filename']
        )

        nlp = nlp.text_cleaner(blob_file['filename'])
        update_record=az.update_cosmos_document('mongo', docs, blob_file, html_text)
        az.print_cosmos_document('mongo', docs, blob_file)
        az.remove_if_exists(blob_file['filename'])

    return True


if __name__ == "__main__":
    main()
