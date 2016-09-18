import sys
import json
import datetime
from datetime import timedelta
from pprint import pprint
from csv import DictReader
from collections import OrderedDict

import pandas
import pandas_datareader.data as web
from scipy import stats



def generate_finance_data(days_ago, stock_ticker):
    today = datetime.date.today()
    start_date = today - timedelta(days=days_ago)
    df = web.DataReader(stock_ticker, "yahoo", start_date, today)

    # Interpolate holidays and weekends
    # ---------------------------------
    missing_date_idx = pandas.date_range(str(df.ix[0].name.date()), str(df.ix[-1].name.date()))
    return df.reindex(missing_date_idx).interpolate()


def generate_date_dict(days_ago):
    """
    Generates a dictionary that will bucket number of posts by day.
    """
    start_date = datetime.date.today() - timedelta(days=days_ago)
    
    date_dict = OrderedDict()
    while start_date < datetime.date.today():
        date_dict[start_date] = 0
        start_date += timedelta(days=1)
    return date_dict


def bucket_posts_by_day(input_csv, days_ago):
    date_dict = generate_date_dict(days_ago)

    f = open(input_csv)
    dict_reader = DictReader(f)

    for ctr, row in enumerate(dict_reader):
        submission_time = int(row['created'])
        converted = datetime.date.fromtimestamp(submission_time)

        try:
            date_dict[converted] += 1
        except KeyError:
            pass
    f.close()
    return date_dict


def main(input_filename, days_ago, stock_ticker, offset):
    if len(set([input_filename, days_ago, stock_ticker])) == 1:
        try:
            input_filename = sys.argv[1]
            stock_ticker = sys.argv[2].upper()
            days_ago = int(sys.argv[3])
            offset = int(sys.argv[4])
        except IndexError:
            print """
            Usage: python gendate.py <input_csv> <stock_ticker> <days_ago>
            Example: python gendate.py chipotle.csv cmg 1200 5
            """

    date_dict = bucket_posts_by_day(input_filename, days_ago+offset)
    finance_frame = generate_finance_data(days_ago + offset, stock_ticker)
    daterange = pandas.date_range(start=str(date_dict.items()[0][0]), end=date_dict.items()[-1][0])
    insta_series = pandas.Series([v for k,v in date_dict.items()], index=daterange)
    finance_frame['NumPosts'] = insta_series
    shifted_frame = finance_frame.NumPosts.shift(offset)


    return finance_frame

if __name__ == '__main__':
    main(None, None, None, None)
