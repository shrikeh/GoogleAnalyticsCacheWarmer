#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'barneyhanlon'

import ga, sys, requests, simplejson
from multiprocessing import Process


def warm_url(url, headers) :
    response = requests.get(url, headers=headers)
    if response.status_code != 200 :
        print 'Received error code ' + str(response.status_code) + ' for url ' + url

def warm_cache(config, url) :
    procs = []

    for server in config['servers'] :
        p = Process(target=warm_url, args=(server['host'] + url, config['headers']))
        procs.append(p)
        p.start()

    for p in procs:
        if p.is_alive():
            p.join()


def main(argv) :
    config = simplejson.load(open('config.json'))
    urls = ga.fetch_urls(config)
    procs = []
    for url in urls :
        target = urls[url]

        p = Process(target=warm_cache, args=(config, target))
        procs.append(p)
        p.start()

    for p in procs:
        if p.is_alive():
            p.join()

if __name__ == '__main__':
    main(sys.argv)
