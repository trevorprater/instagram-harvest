import os,sys
reload(sys)
sys.setdefaultencoding('utf-8')
from pprint import pprint

import pika
import psycopg2
import ujson as json

import getphotos

RMQ_CREDS = pika.PlainCredentials('youfie', '977fd7b6-bfea-494b-b818-1f90930dbdad')
RMQ_CONN = pika.BlockingConnection(pika.ConnectionParameters('192.34.57.93',5672,'/', RMQ_CREDS))
RMQ_CHANNEL = RMQ_CONN.channel()

def callback(ch, method, properties, body):
    body = json.loads(body)
    ch.basic_publish(exchange='', routing_key='responses', body=json.dumps(getphotos.request_location_page(body['id'])))
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    RMQ_CHANNEL.basic_consume(callback, queue='testqueue')
    RMQ_CHANNEL.start_consuming()

if __name__ == '__main__':
    main()
