#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import subprocess
import time
from pprint import pprint

import requests
from bs4 import BeautifulSoup as BS
import json

BASE_URL = 'https://www.instagram.com/explore/locations/{}'

CURL = """curl -s 'https://www.instagram.com/query/' --max-time 10 --retry 5 --retry-delay 0 --retry-max-time 60 -H 'origin: https://www.instagram.com' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: en-US,en;q=0.8' -H 'x-requested-with: XMLHttpRequest' -H 'cookie: csrftoken={}' -H 'x-csrftoken: {}' -H 'pragma: no-cache' -H 'x-instagram-ajax: 1' -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36' -H 'content-type: application/x-www-form-urlencoded' -H 'accept: */*' -H 'cache-control: no-cache' -H 'authority: www.instagram.com' -H 'referer: https://www.instagram.com/explore/locations/{}/' --data 'q=ig_location({})+%7B+media.after({}%2C+{})+%7B%0A++count%2C%0A++nodes+%7B%0A++++caption%2C%0A++++code%2C%0A++++comments+%7B%0A++++++count%0A++++%7D%2C%0A++++date%2C%0A++++dimensions+%7B%0A++++++height%2C%0A++++++width%0A++++%7D%2C%0A++++display_src%2C%0A++++id%2C%0A++++is_video%2C%0A++++likes+%7B%0A++++++count%0A++++%7D%2C%0A++++owner+%7B%0A++++++id%0A++++%7D%2C%0A++++thumbnail_src%2C%0A++++video_views%0A++%7D%2C%0A++page_info%0A%7D%0A+%7D&ref=locations%3A%3Ashow' --compressed"""

def request_location_page(location_id):
    s = requests.Session()
    s.headers.update({'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'})
    num_attempts = 3
    attempt = 0
    backoff = 1
    url = BASE_URL.format(location_id)
    while attempt < num_attempts:
        r = s.get(url)
        if r.status_code == 429:
            attempt += 1
            time.sleep(backoff)
            backoff *= 2
        else:
            break
        if attempt == num_attempts - 1:
            raise Exception('Tried too many times! 429 received')
    try:
        r.raise_for_status()
    except Exception as e:
        print e
        return

    bs = BS(r.content, "lxml")
    text = bs.get_text()
    startndx = text.find('_sharedData = ') + len('_sharedData = ')
    substr = text[startndx:]
    _json = substr[:substr.find('};')+1]
    data = json.loads(_json)
    endcursor = data['entry_data']['LocationsPage'][0]['location']['media']['page_info']['end_cursor']
    photos = {}
    initial_photos = data['entry_data']['LocationsPage'][0]['location']['media']['nodes']
    if 'top_posts' in data['entry_data']['LocationsPage'][0]['location'].keys():
        initial_photos.extend(data['entry_data']['LocationsPage'][0]['location']['top_posts']['nodes'])
    if len(initial_photos) > 0:
        for photo in initial_photos:
            photos[photo['code']] = photo
    oldLen = len(photos.keys())
    while(True):
        csrf = s.cookies['csrftoken']
        exec_str = CURL.format(csrf, csrf, location_id, location_id, endcursor, 50)
        resp = os.popen(exec_str).read()
        data = json.loads(resp)
        endcursor = data['media']['page_info']['end_cursor']
        if len(data['media']['nodes']) > 0:
            for photo in data['media']['nodes']:
                photos[photo['code']] = photo
        if not len(photos.keys()) > oldLen:
            break
        oldLen = len(photos.keys())

    photos = [photos[k] for k,v in photos.iteritems()]
    output = json.dumps(photos, indent=4)
    print output
    return photos


if __name__ == '__main__':
    request_location_page(int(sys.argv[1]))
