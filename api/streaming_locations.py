#!/usr/bin/env python

# Copyright 2015, Google, Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Command-line application that streams data into BigQuery.

This sample is used on this page:

    https://cloud.google.com/bigquery/streaming-data-into-bigquery

For more information, see the README.md under /bigquery.
"""
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

import argparse
import ast
import json
import uuid

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials
from six.moves import input

BATCH_SIZE = 1000

# [START stream_row_to_bigquery]
def stream_row_to_bigquery(bigquery, project_id, dataset_id, table_name, rows,
                           num_retries=5):
    insert_all_data = {
        'rows': [{
            'json': row,
            # Generate a unique id for each row so retries don't accidentally
            # duplicate insert
            'insertId': str(uuid.uuid4()),
        } for row in rows]
    }
    return bigquery.tabledata().insertAll(
        projectId=project_id,
        datasetId=dataset_id,
        tableId=table_name,
        body=insert_all_data).execute(num_retries=num_retries)


def main(project_id, dataset_id, table_name, num_retries):
    # Grab the application's default credentials from the environment.
    credentials = GoogleCredentials.get_application_default()

    # Construct the service object for interacting with the BigQuery API.
    bigquery = discovery.build('bigquery', 'v2', credentials=credentials)

    ctr = 0
    _rows = []
    for row in get_rows():
        _rows.append(row)
        ctr += 1
        if ctr > BATCH_SIZE:
            response = stream_row_to_bigquery(bigquery, project_id, dataset_id, table_name, _rows, num_retries)
            print(json.dumps(response))
            ctr = 0
            _rows = []
    response = stream_row_to_bigquery(bigquery, project_id, dataset_d, table_name, _rows, num_retries)
    print(json.dumps(response))


def get_rows():
    CUR.execute("SELECT * FROM location;")
    res = CUR.fetchone()
    while res:
        pprint(res)
        if not res['name']:
            res = CUR.fetchone()
            continue
        if res['lat']:
            lat = str(res['lat'])
        else:
            lat = '-1'
        if res['lng']:
            lng = str(res['lng'])
        else:
            lng = '-1'
        if '.' in lat:
            if len(lat[lat.find('.'):]) > 6:
                lat = lat[:lat.find('.')+5]
        if '.' in lng:
            if len(lng[lng.find('.'):]) > 6:
                lng = lng[:lng.find('.')+5]
        yield {'name':res['name'], 'id': int(str(res['id'])), 'lat': float(lat), 'lng': float(lng)}
        res = CUR.fetchone()
    DB_CONN.close()


# [START main]
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project_id', help='Your Google Cloud project ID.')
    parser.add_argument('dataset_id', help='A BigQuery dataset ID.')
    parser.add_argument(
        'table_name', help='Name of the table to load data into.')
    parser.add_argument(
        '-p', '--poll_interval',
        help='How often to poll the query for completion (seconds).',
        type=int,
        default=1)
    parser.add_argument(
        '-r', '--num_retries',
        help='Number of times to retry in case of 500 error.',
        type=int,
        default=5)

    args = parser.parse_args()

    main(
        args.project_id,
        args.dataset_id,
        args.table_name,
        args.num_retries)
# [END main]
