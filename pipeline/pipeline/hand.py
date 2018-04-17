import time
import requests
import os


_url = os.environ['HAND_URL']
_key = os.environ['HAND_KEY']
_maxNumRetries = 10


def get_hand_location(json, data, headers, params):
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
        response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )

        if response.status_code == 429:
            print( "Message: %s" % ( response.json() ) )
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
            print( "Message: %s" % ( response.json() ) )
        break
    return result


def get_hand_text(location, headers):
    """
    Helper function to get text result from operation location

    Parameters:
    location: operationLocation to get text result, See API Documentation
    headers: Used to pass the key information
    """
    retries = 0
    result = None

    while True:
        response = requests.request('get', location, json=None, data=None, headers=headers, params=None)
        if response.status_code == 429:
            print("Message: %s" % (response.json()))
            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print('Error: failed after retrying!')
                break
        elif response.status_code == 200:
            result = response.json()
        else:
            print("Error code: %d" % (response.status_code))
            print("Message: %s" % (response.json()))
        break

    return result


def extract_hand_text(imgs):
    """Extract handwriting from list of PIL JPG images

    Convert a set of PIL JPG images to a list of extracted text
    Inputs:
        imgs: List of PIL JPGs
    Outputs:
        d: List of extracted text
    """
    text_list=[]
    for i in imgs:
        i.save('test.jpg')
        with open('test.jpg', 'rb') as f:
            data = f.read()

        # Computer Vision parameters
        params = {'handwriting' : 'true'}

        headers = dict()
        headers['Ocp-Apim-Subscription-Key'] = _key
        headers['Content-Type'] = 'application/octet-stream'

        json = None
        location = get_hand_location(json, data, headers, params)

        result = None
        if (location != None):
            headers = {}
            headers['Ocp-Apim-Subscription-Key'] = _key
            while True:
                time.sleep(1)
                result = get_hand_text(location, headers)
                if result['status'] == 'Succeeded' or result['status'] == 'Failed':
                    res = result['recognitionResult']
                    for line in res['lines']:
                        for word in line['words']:
                            text_list.append((word['text']))
                    break

    d = {'extracted_hand': text_list}
    return d

