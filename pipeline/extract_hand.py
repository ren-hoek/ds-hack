from pipeline import azure as az
from pipeline import hand as hd
from pipeline import ocr

def main():
    docs = az.get_cosmos_collection('mongo', 'ch', 'docs')
    ch = az.AzureBlob('ch')
    blob_files = docs.find({'filetype': 'pdf', 'doctype': 'annual-returns'})

    for i, blob_file in enumerate(blob_files):
        if i>4:
            break
        print(blob_file['container'], blob_file['blob_file'])

        ch.blob.get_blob_to_path(
            blob_file['container'],
            blob_file['blob_file'],
            blob_file['filename']
        )

        pages = ocr.create_jpg(blob_file['filename'])
        print(pages['page_count'])
        hand_text = hd.extract_hand_text(pages['pages'])
        update_record=az.update_cosmos_document('mongo', docs, blob_file, hand_text)
        az.print_cosmos_document('mongo', docs, blob_file)

        az.remove_if_exists(blob_file['filename'])
        az.remove_if_exists('test.jpg')

    return True


if __name__ == "__main__":
    main()

