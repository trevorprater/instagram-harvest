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



def generate_finance_data(end_day, days_ago, stock_ticker):
    start_date = end_day - timedelta(days=days_ago)
    return web.DataReader(stock_ticker, "yahoo", start_date, end_day)


def generate_date_dict(end_day, days_ago):
    """
    Generates a dictionary that will bucket number of posts by day.
    """
    start_date = end_day - timedelta(days=days_ago)
    
    date_dict = OrderedDict()
    while start_date < end_day:
        date_dict[str(start_date)] = 0
        start_date += timedelta(days=1)
    
    return date_dict


def bucket_posts_by_day(end_day, input_csv, num_days_ago):
    date_dict = generate_date_dict(end_day, num_days_ago)

    f = open(input_csv)
    dict_reader = DictReader(f)

    for ctr, row in enumerate(dict_reader):
        # Get the time the photo was posted.
        submission_time = int(row['created'])

        # Convert the time to a date object, the same datatype as
        # the keys in our date_dict.
        converted = str(datetime.date.fromtimestamp(submission_time))

        # Increment the number of photos posted on date.
        try:
            date_dict[converted] += 1
        except KeyError:
            # If a KeyError is thrown, this date is not in our date_dict,
            # which means we didn't pass in a large enough value to
            # generate_date_dict.
            pass
    f.close()

    return date_dict
    

def calculate_avg_price(day1, day2):
    pass


def get_last_valid_finance_day(stock_ticker):
    today = datetime.date.today()
    data = generate_finance_data(today, 7, stock_ticker)
    return data.ix[-1].name.date()


def get_first_valid_date_from_csv(date_dict):
    return date_dict.items()[0][0]


def clean_date_dict(date_dict):
    items = date_dict.items()
    items.reverse()
    for date, num_posts in items:
        if num_posts > 0:
            return date_dict
        del date_dict[date]


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
            Example: python gendate.py chipotle.csv cmg 1200 -5
            """

    last_open_day = get_last_valid_finance_day(stock_ticker)
    today = datetime.date.today()

    date_dict = bucket_posts_by_day(last_open_day, input_filename, days_ago)
    date_dict = clean_date_dict(date_dict)
    del date_dict[date_dict.keys()[-1]]
    finance_frame = generate_finance_data(last_open_day, days_ago, stock_ticker)

    joined_data = {}
    num_posts_list, prices = ([],[])

    for date, num_posts in date_dict.items():
        try:
            frame = finance_frame.ix[date]
            closing_price = frame.ix['Close']
            joined_data[date] = (date_dict[date], closing_price)

            num_posts_list.append(num_posts)
            prices.append(closing_price)

        except KeyError as e:
            pass

    linregress = stats.linregress(num_posts_list, prices)
    slope, intercept, r_value, p_value, std_err = linregress
    
    joined_data['stats'] = {
            'r^2': r_value**2,
            'slope': slope,
            'intercept': intercept,
            'r_value': r_value,
            'p_value': p_value,
            'std_err': std_err
    }

    return joined_data

if __name__ == '__main__':
    main(None, None, None)
