#!/usr/bin/env python

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.
import requests
from pprint import pprint
import json
import base64
import webbrowser

#don't change this
URL = r'http://api.imgur.com/2/upload.json'

#replace this next line to look like:
#KEY = "my_imgur_api_key"
KEY = None 

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
    from optparse import OptionParser
    from sys import argv, exit

    if KEY == None:
        exit("Please go get an imgur api key\n\tapi.imgur.com\n\tsee README for details")

    usage = "{name} [options] image".format(name=argv[0])

    parser = OptionParser(usage=usage)

    parser.add_option("-p", "--print",
            dest="is_print", help="make the program print the imgur urls",
            action="store_true", default=False)

    parser.add_option("-j", "--json",
            dest="is_json", help="pretty print the json from the upload",
            action="store_true", default=False)

    parser.add_option("-n", "--no-open",
            dest="is_should_open", help="don't open in your web browser",
            action="store_false", default=True)

    parser.add_option("-t", "--title",
            dest="title", help="optional title for your upload", default=None)


    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error("need an image bro")

    r = upload(args[0], title=options.title)
    j = json.loads(r.text)
    urls = j["upload"]["links"]

    if options.is_should_open:
        webbrowser.open_new(urls["imgur_page"])
    if options.is_json:
        pprint(j)
    if options.is_print:
        for name, link in urls.iteritems():
            print name, "=>", link

