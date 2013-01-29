#!/usr/bin/python
__author__ = 'barneyhanlon'
# -*- coding: utf-8 -*-
# import required classes
import httplib2
from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

def prepare_credentials(secrets_file, storage_file):
    # Retrieve existing credendials
    storage = Storage(storage_file)
    credentials = storage.get()

    # If existing credentials are invalid and Run Auth flow
    # the run method will store any new credentials
    if credentials is None or credentials.invalid:
        # A file to store the access token

        # The Flow object to be used if we need to authenticate.
        flow = flow_from_clientsecrets(
            secrets_file,
            scope='https://www.googleapis.com/auth/analytics.readonly',
            message='%s is missing' % secrets_file
        )
        credentials = run(flow, storage) #run Auth Flow and store credentials

    return credentials


def initialize_service(secrets_file, storage_file):
    # 1. Create an http object
    http = httplib2.Http()

    # 2. Authorize the http object
    # In this tutorial we first try to retrieve stored credentials. If
    # none are found then run the Auth Flow. This is handled by the
    # prepare_credentials() function defined earlier in the tutorial
    credentials = prepare_credentials(secrets_file, storage_file)
    http = credentials.authorize(http)  # authorize the http object

    # 3. Build the Analytics Service Object with the authorized http object
    return build('analytics', 'v3', http=http)

