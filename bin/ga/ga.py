import analytics_auth

__author__ = 'barneyhanlon'
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
# import the Auth Helper class

from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError

def fetch_urls(storage_file, secrets_file, profile_id, max_results, days, verbosity=0):
    """
    Authenticate with Google Analytics using oAuth and fetch the top
    n popular pages over n days from Google Analytics
    """
    # Step 1. Get an analytics service object.
    service = analytics_auth.initialize_service(
        storage_file=storage_file,
        secrets_file=secrets_file
    )
    try:
        if verbosity > 0:
            print 'Fetching ' + str(max_results) + ' results for the last ' + str(days) + ' days'
            # Step 3. Query the Core Reporting API.
            results = get_results(
                service=service,
                profile_id=profile_id,
                max_results=max_results,
                days=days
            )
            # Step 4. Output the results.
            return parse_results(results)
    except TypeError, error:
        # Handle errors in constructing a query.
        print ('There was an error in constructing your query : %s' % error)

    except HttpError, error:
        # Handle API errors.
        print ('Arg, there was an API error : %s : %s' %
               (error.resp.status, error._get_reason()))

    except AccessTokenRefreshError:
        # Handle Auth errors.
        print ('The credentials have been revoked or expired, please re-run '
               'the application to re-authorize')

#def get_first_profile_id(service):
    # Get a list of all Google Analytics accounts for this user
#    accounts = service.management().accounts().list().execute()
#
#    if accounts.get('items'):
        # Get the first Google Analytics account
        # Get a list of all the Web Properties for the first account
#        webproperties = service.management().webproperties().list(accountId=25058877).execute()
#        if webproperties.get('items'):
            # Get the first Web Property ID
#            for items in webproperties.get('items') :
#                if 'UA-25058877-6' == items.get('id') :
#                    # Get a list of all Profiles for the first Web Property of the first Account
#                    profiles = service.management().profiles().list(
#                    accountId=25058877,
#                    webPropertyId='UA-25058877-6').execute()

#                    if profiles.get('items'):
#                        for profile in profiles.get('items') :
#                            if 'Unfiltered Profile' == profile.get('name') :
#                                print profile.get('id')
#                                return profile.get('id')

#    return None

def get_results(service, profile_id, max_results=100, days=1):
    """
    Use the Analytics Service Object to query the Core Reporting API
    """
    # Use the Analytics Service Object to query the Core Reporting API

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    return service.data().ga().get(
        ids='ga:' + profile_id,
        dimensions='ga:pagePath',
        start_date=start_date.strftime('%Y-%m-%d'),
        end_date=end_date.strftime('%Y-%m-%d'),
        metrics='ga:visits',
        sort='-ga:visits',
        max_results=max_results
    ).execute()

def parse_results(results, filters={}):
    """
    Parse through the URLs collected and create an array
    """
    # Print data nicely for the user.
    if results:
        print 'First Profile: %s' % results.get('profileInfo').get('profileName')
        try :
            urls = {}
            for page in results.get('rows') :
            # OK, now go through the list of URLs
                if page[0]:
                    urls[page[0]] = page[0]
            return urls
        except TypeError :
            print 'No visits'
    else:
        print 'No results found'


