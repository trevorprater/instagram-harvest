# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import calendar

def format_photo_for_db(photo_dict):
    d = {}
    d['id'] = photo_dict['id']
    d['caption'] = photo_dict.get('caption', '').replace("'","''")
    d['pcode'] = photo_dict['code']
    d['comments'] = photo_dict['comments']['count']
    d['created'] = photo_dict['date'] 
    d['updated'] = calendar.timegm(time.gmtime())
    d['is_vid'] = photo_dict['is_video']
    d['likes'] = photo_dict['likes']['count']
    d['owner_id'] = photo_dict['owner']['id']
    d['url'] = photo_dict['display_src']
    d['location_id'] = photo_dict.get('location_id', -1)
    return d

