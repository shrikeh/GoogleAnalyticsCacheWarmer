#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'barneyhanlon'

import sys, argparse
from warmer import warmer

def main(argv):

    parser = argparse.ArgumentParser(
        description='Fetch the latest n most visited URLs on your site (as reported by Google Analytics), and then pre-warm their cache'
    )
    parser.add_argument(
        '-v',
        "--verbose",
        action="count",
        help="increase output verbosity",
    )
    parser.add_argument(
        '-p',
        '--profile',
        metavar='<profile_id>',
        help='The profile ID for Google Analytics to query'
    )
    parser.add_argument(
        '-c',
        '--config',
        metavar='<config_file>',
        default='./config.json',
        help='The config file to use'
    )
    parser.add_argument(
        '-f',
        '--filters',
        metavar='<python module>',
        help='If you wish to run modifications to URLs after collecting, the filter to run'
    )
    parser.add_argument(
        '-a',
        '--auth',
        metavar='<secrets_file>',
        default='./client_secrets.json',
        help='The config file to use for oAuth'
    )
    parser.add_argument(
        '-w',
        '--storage',
        metavar='<storage_file>',
        default='./analytics.dat',
        help='Where to write GA authentication to'
    )
    parser.add_argument(
        '-d',
        '--days',
        metavar='N',
        type=int,
        default=1,
        help='the number of days to use to get the highest rated pages. Defaults to 1'

    )
    parser.add_argument(
        '-r',
        '--results',
        metavar='N',
        type=int,
        default=100,
        help='an integer representing the number of results to fetch from Google Analytics')
    args = parser.parse_args()

    warmer(
        config_file=args.config,
        storage_file=args.storage,
        secrets_file=args.auth,
        profile_id=args.profile,
        verbosity=args.verbose,
        days=args.days,
        max_results=args.results,
        filters=args.filters
    )

if __name__ == '__main__':
    main(sys.argv)
