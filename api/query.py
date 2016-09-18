import os,sys
reload(sys)
sys.setdefaultencoding('utf-8')
from pprint import pprint

import psycopg2
from psycopg2.extras import RealDictCursor
import json

CONN_STRING = "host='localhost' dbname='locations' user='postgres' password='89347598204alkegohlw33LKJI23dflkj'"
DB_CONN = psycopg2.connect(CONN_STRING)
CUR = DB_CONN.cursor('querycursor', cursor_factory=RealDictCursor)
CUR.execute("SELECT * FROM location limit 1")
outf=open('photos.json','w+')

res = CUR.fetchone()
while res:
    pprint(dict(res))
    #outf.write(json.dumps(dict(res))+'\n')
    ##res = CUR.fetchone()

DB_CONN.close()
outf.close()
