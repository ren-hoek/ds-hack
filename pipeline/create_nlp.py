from pipeline import azure as az
from pipeline import nlp


def main():
    docs = az.get_cosmos_collection('mongo', 'ch', 'docs')
    ch = az.AzureBlob('ch')
    blob_files = docs.find({
        'filetype': 'xhtml',
        'extracted_html': {'$exists': True}
    })

    for i, blob_file in enumerate(blob_files):
        if i>4:
            break

        nlp_extract = nlp.text_cleaner(" ".join(blob_file['extracted_html']))
        update_record=az.update_cosmos_document('mongo', docs, blob_file, nlp_extract)
        az.print_cosmos_document('mongo', docs, blob_file)

    return True


if __name__ == "__main__":
    main()

