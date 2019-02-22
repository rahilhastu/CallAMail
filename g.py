#!/usr/bin/env python3

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json
import calltest
import logging
import datetime

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """
        Logging info
    """
    logging.basicConfig(level=logging.DEBUG, filename= 'rahilGmail.log')

    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_id.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    # print (json.dumps(labels,indent=4))

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            if label['name']=='PES/PESIT Placement':
                print(label['name']+"---"+label['id'])
                inf = service.users().labels().get(userId='me',id=label['id']).execute()    
                # info = json.dumps(inf,indent=4)
                count_unread = inf['messagesUnread']
                print(count_unread)
                if count_unread:
                    try:
                        print("There are %d messages unread"%(count_unread))
                        calltest.main()
                    except:
                        print("There are unread messages but Call cannot be placed!")
                else:
                    print("No unread messages")
        logging.debug("\nThere are "+str(count_unread)+" messages unread at time "+str(datetime.datetime.now())+"\n\n"+"*"*90+"\n")

if __name__ == '__main__':
    main()
