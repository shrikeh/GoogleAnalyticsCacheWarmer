__author__ = 'barneyhanlon'

import sys, requests, simplejson, imp
from ga import ga
from multiprocessing import Process
from traceback import format_exc

def warm_url(url, headers, verbosity=0):
    """
    Warms a specific URL on a specific web head
    """
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200 and verbosity > 0:
            print 'Received error code ' + str(response.status_code) + ' for url ' + url
    except requests.ConnectionError:
        print format_exc()


def warm_cache(servers, headers, url, verbosity=0):
    """
    Takes a target URL and hits every registered load balancer with the given URL
    """
    procs = []
    for server in servers :
        p = Process(target=warm_url, args=(server['host'] + url, headers, verbosity))
        procs.append(p)
        p.start()

    for p in procs:
        if p.is_alive():
            p.join()

def process(urls, servers, headers, filters, verbosity):
    procs = []
    if urls:
        moduleobj = None
        if filters:
            fileobj, pathname, description = imp.find_module(filters)
            moduleobj = imp.load_module(filters, fileobj, pathname, description)
            fileobj.close()

        for url in urls:
            target = urls[url]
            if moduleobj:
                target = moduleobj.parse_url(target)
            if url:
                p = Process(target=warm_cache, args=(
                    servers,
                    headers,
                    target,
                    verbosity
                ))
                procs.append(p)
                p.start()
                # Loop through all the processes...
        for p in procs:
            if p.is_alive():
                # Wait till it's over...
                p.join()


def warmer(
        config_file,
        storage_file,
        secrets_file,
        profile_id,
        verbosity,
        days,
        max_results,
        filters
):
    """
    Attempts to fetch n URLs from Google Analytics ordered by most visited,
    and then hits each load balancer with that URL, allowing cache warming
    """
    config = simplejson.load(open(config_file))

    if not config['client']:
        config['client'] = []

    if storage_file:
        config['client']['storage'] = storage_file
    if secrets_file:
        config['client']['secrets_file'] = secrets_file

    if not profile_id:
        profile_id = config['profile']['id']

    if not max_results:
        if config['max_results']:
            max_results = config['max_results']
        else :
            max_results = 100


    urls = ga.fetch_urls(
        storage_file=config['client']['storage'],
        secrets_file=config['client']['secrets_file'],
        profile_id=profile_id,
        max_results=max_results,
        days=days,
        verbosity=verbosity
    )
    process(urls, config['servers'], config['headers'], filters, verbosity)
