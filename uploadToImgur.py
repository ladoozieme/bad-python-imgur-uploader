import requests
import os
from pprint import pprint
import json
import sys
import base64

URL = r'http://api.imgur.com/2/upload.json'
KEY = 'c9f580e62318a665305d47ca4931e90e'

def upload(fp, title=None):
    global URL
    global KEY
    try:
        with open(fp, 'rb') as f: #reading binary data
            bin_data = base64.b64encode(f.read())
    except IOError:
        print "That file doesn't exist maybe you typed it wrong"
        sys.exit(1)

    payload = {'key': KEY,
            'image': bin_data}
    if title: payload['title'] = title

    r = requests.post(URL, data=payload)
    return r


if __name__ == '__main__':
    argc = len(sys.argv)
    if argc < 2:
        print "USAGE: image [title]"
        sys.exit(1)

    image = sys.argv[1]
    
    if argc > 2:
        title = ' '.join(sys.argv[2:])
    else:
        title = None


    r = upload(image, title=title)
    j = json.loads(r.text)
    with open('test.json', 'w+') as f:
        json.dump(r.text, f, indent=4)

    pprint(j)
    for name, link in j['upload']['links'].iteritems():
        print name.upper(), ' => ', link

