# -*- coding: utf-8 -*-
"""
Retreive current exchange rate for specified currencies
using https://www.exchangerate-api.com/ APIs.
"""
import argparse
from os import getenv

import requests


exchangerate_error_codes = {
        'unknown-code': "Don't support either of the supplied currency codes",
        'invalid-key': "Key isn't active or doesn't exist",
        'malformed-request': "Malformed request",
        'quota-reached': "Your account runs out of request quota"
        }


def get_rate(url):
    rate = requests.get(url)

    if rate.status_code != 200:
        raise Exception(
                f'HTTP Exception occured, status code: {rate.status_code}')

    data = rate.json()

    if 'error' in data.keys():
        print(exchangerate_error_codes[data['error']])
        exit(1)

    return data['rate']


def get_url(api_key, base_cur, conv_cur):
    return '/'.join(['https://v3.exchangerate-api.com/pair', api_key,
                    base_cur.upper(), conv_cur.upper()])


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('base', help='base currency')
    parser.add_argument('to', help='convert currency')
    parser.add_argument('-k', '--key', default=getenv('ER_KEY', ''),
                        help='your exchangerate-api API key')

    parsed_args = parser.parse_args()
    if parsed_args.key == '':
        print('Please, set either ER_KEY env variable, or put '
              'exchangerate-api API key explicitly using --key argument')
        exit(1)

    return parsed_args


if __name__ == '__main__':
    args = parse()
    url = get_url(args.key, args.base, args.to)
    rate = get_rate(url)

    print(rate)
