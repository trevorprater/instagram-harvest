import os,sys
reload(sys)
sys.setdefaultencoding('utf-8')
from datetime import datetime
import calendar
import time
import psycopg2


CONN_STRING = "host='localhost' dbname='locations' user='postgres' password='89347598204alkegohlw33LKJI23dflkj'"
DB_CONN = psycopg2.connect(CONN_STRING)
QUERY = "SELECT COUNT(1) from photo;"
CUR = DB_CONN.cursor()
SLEEP = 10

old_amt = -sys.maxint
while 1:
    now = int(calendar.timegm(time.gmtime()))
    CUR.execute(QUERY)
    query_time = (int(calendar.timegm(time.gmtime())) - now)
    res = int(CUR.fetchall()[0][0])
    delta = (res - old_amt)
    old_amt = res
    print '{} photos @ {}/second'.format(res,delta / SLEEP)
    time.sleep(SLEEP - query_time)
