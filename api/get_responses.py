# -*- coding: utf-8 -*-

import os,sys
reload(sys)
sys.setdefaultencoding('utf-8')
from pprint import pprint

import psycopg2
import ujson as json
import beanstalkc

from util import util

CONN_STRING = "host='localhost' dbname='locations' user='postgres' password='89347598204alkegohlw33LKJI23dflkj'"
DB_CONN = psycopg2.connect(CONN_STRING)
DB_CURSOR = DB_CONN.cursor()
BS = beanstalkc.Connection(host='192.241.128.251', port=11300)
INSERT_QUERY = """INSERT INTO photo
    (id, pcode, owner_id, location_id, caption, likes, comments, created, updated, is_vid, url)
    VALUES
        ({}, '{}', {}, {}, '{}', {}, {}, {}, {}, {}, '{}')
        ON
            CONFLICT (id)
            DO UPDATE SET
                pcode = EXCLUDED.pcode,
                location_id = EXCLUDED.location_id,
                caption = EXCLUDED.caption,
                likes = EXCLUDED.likes,
                comments = EXCLUDED.comments,
                created = EXCLUDED.created,
                updated = EXCLUDED.updated,
                is_vid = EXCLUDED.is_vid,
                url = EXCLUDED.URL;"""



def main():
    try:
        while 1:
            job = BS.reserve()
            job.delete()
            print_completed(job.body)

    except Exception as e:
        print e
        exit()

def print_completed(body):
    photo = json.loads(body)
    pprint(photo)
    if photo:
        dbp = util.format_photo_for_db(photo)
        query = INSERT_QUERY.format(dbp['id'],dbp['pcode'],dbp['owner_id'], dbp['location_id'], dbp['caption'], dbp['likes'], dbp['comments'], dbp['created'], dbp['updated'], dbp['is_vid'], dbp['url'])
        try:
            DB_CURSOR.execute(query.encode('utf-8'))
        except Exception as e:
            print e
            DB_CONN.commit()
    DB_CONN.commit()

def exit():
    DB_CONN.close()

if __name__ == '__main__':
    main()
