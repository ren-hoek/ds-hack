import os
import io
from PIL import Image
import wand.image as wd
import requests
import time


_url = os.environ['VISION_URL']
_key = os.environ['VISION_KEY']
_maxNumRetries = 10


def create_jpg(f):
    """Create multipage JPG from PDF.

    Create a JPG object from a local PDF file
    Input:
        f: Local path to PDF file
    Output:
        d: Dictionary of JPG objects
    """
    d = dict()
    filepath = f
    assert os.path.exists(f)
    with wd.Image(filename=f, resolution=200) as img:
        page_images = []
        for page_wand_image_seq in img.sequence:
            page_wand_image = wd.Image(page_wand_image_seq)
            page_jpeg_bytes = page_wand_image.make_blob(format="jpeg")
            page_jpeg_data = io.BytesIO(page_jpeg_bytes)
            page_image = Image.open(page_jpeg_data)
            page_images.append(page_image)
    d['page_count'] = len(page_images)
    d['pages'] = page_images
    return d


def process_request( json, data, headers, params ):
    """
    Helper function to process the request to Project Oxford

    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:
        response = requests.request(
                'post',
                _url,
                json = json,
                data = data,
                headers = headers,
                params = params
        )

        if response.status_code == 429:
            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print( 'Error: failed after retrying!' )
                break
        elif response.status_code == 202:
            result = response.headers['Operation-Location']
        else:
            print( "Error code: %d" % ( response.status_code ) )
        break
    return response.json()


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


def extract_ocr_text(imgs):
    """Extract ocr text from images.

    Extract handwritten text from a set of JPG images
    Input:
        imgs: List of PIL image files
    Output:
        d: K-V pair (extracted_ocr: List of text
    """
    params = {'handwriting' : 'true'}
    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _key
    headers['Content-Type'] = 'application/octet-stream'
    json = None

    API_call_flat = []

    for i in imgs:
        i.save('test.jpg')
        with open('test.jpg', 'rb') as f:
            data = f.read()
        API_call = process_request(json, data, headers, params)
        API_call_flat.append(list(find('text', API_call)))

    extracted_hand = [x for y in API_call_flat for x in y]

    d = dict()
    d['extracted_ocr'] = extracted_hand
    return d
