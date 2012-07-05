#!/usr/bin/env python

# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.
import requests
from pprint import pprint
import json
from sys import argv, exit
import base64
import webbrowser

#don't change this
URL = r'http://api.imgur.com/2/upload.json'

#replace this next line to look like:
#KEY = "my_imgur_api_key"
KEY = None 

def upload(fp, title=None, caption=None, name=None):
    """read a file encode it as bas64 upload it to imgur
    and return a requests response object"""
    with open(fp, 'rb') as f: #reading binary data
        bin_data = base64.b64encode(f.read())

    payload = {'key': KEY,
            'image': bin_data}
    if title: payload['title'] = title
    if caption: payload['caption'] = caption
    if name: payload['name'] = name

    r = requests.post(URL, data=payload)
    return r


if __name__ == '__main__':
    from optparse import OptionParser

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

    parser.add_option("-w", "--no-web-browser",
            dest="is_should_open", help="don't open in your web browser",
            action="store_false", default=True)

    parser.add_option("-t", "--title",
            dest="title", help="optional title for your upload", default=None)

    parser.add_option("-n", "--name",
            dest="name", help="optional name for the image", default=None)

    parser.add_option("-c", "--caption",
            dest="caption", help="optional caption for the image", default=None)


    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.error("need an image bro")

    r = upload(args[0], title=options.title, name=options.name, caption=options.caption)
    j = json.loads(r.text)
    urls = j["upload"]["links"]

    if options.is_should_open:
        webbrowser.open_new(urls["imgur_page"])
    if options.is_json:
        pprint(j)
    if options.is_print:
        for name, link in urls.iteritems():
            print name, "=>", link

