import os,sys
reload(sys)
sys.setdefaultencoding('utf-8')
from pprint import pprint

#import pika
import psycopg2
from psycopg2.extras import RealDictCursor
import ujson as json
import beanstalkc

CONN_STRING = "host='localhost' dbname='locations' user='postgres' password='89347598204alkegohlw33LKJI23dflkj'"
DB_CONN = psycopg2.connect(CONN_STRING)
BS = beanstalkc.Connection(host='162.243.164.5', port=11300)

#RMQ_CREDS = pika.PlainCredentials('youfie', '977fd7b6-bfea-494b-b818-1f90930dbdad')
#RMQ_CONN = pika.BlockingConnection(pika.ConnectionParameters('198.211.100.217',5672,'/', RMQ_CREDS))
#RMQ_CHANNEL = RMQ_CONN.channel()

def submit_job(query):
    cur = DB_CONN.cursor('querycursor',cursor_factory=RealDictCursor)
    cur.execute(query)
    num_results = 0

    res = cur.fetchone()
    while res:
        # submit job to rabbit mq
        #RMQ_CHANNEL.basic_publish(exchange='', routing_key='testqueue', body=json.dumps(dict(res)))
        print 'submitting job -> numresults: {}'.format(num_results)
        print BS.put(json.dumps(dict(res)))
        num_results += 1
        res = cur.fetchone()
    print 'num results: {}'.format(num_results)
    exit()

def exit():
#    RMQ_CONN.close()
    DB_CONN.close()

if __name__ == '__main__':
    #BS.use('requests')
    submit_job(sys.argv[1])

