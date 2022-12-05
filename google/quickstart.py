from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/directory.readonly','https://www.googleapis.com/auth/contacts.readonly']

def main():

    codigos = []


    """Shows basic usage of the People API.
    Prints the name of the first 10 connections.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                r'C:\Users\ivanr\OneDrive\Desktop\ESTUDIO_TRABAJO\PROYECTOS PROGRAMING\POESISMO DATA\google\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        people_service = build('people', 'v1', credentials=creds)

        # Call the People API
        # print('List 10 connection names')
        results = people_service.people().connections().list(
            resourceName='people/me',
            pageSize=1000,
            personFields='names,organizations').execute()
        connections = results.get('connections', [])
        # print(connections)

# ESTO DE ABAJO ES UNA HTTP REQUEST
        nextPageToken = None
        for i in range(50):
            results2 = people_service.people().listDirectoryPeople(
                sources=['DIRECTORY_SOURCE_TYPE_DOMAIN_PROFILE'],
                readMask='organizations',
                pageSize=1000,
                pageToken=nextPageToken,
            ).execute()
            connections2 = results2.get('people', [])
            nextPageToken=results2.get('nextPageToken')
            for person in connections2:
                codes = person.get('organizations', [])
                if codes:
                    try:
                        if (codes[0].get('title', [])).isnumeric():
                            codigos.append(codes[0].get('title', []))
                    except: pass

    except HttpError as err:
        print(err)
    print(len(codigos))
    return codigos
if __name__ == '__main__':
    codecci = main()
    # print(codecci)
    with open('codigos_uao.txt', 'a+') as f:
        for i in codecci:
            if i not in f.read().split():
                f.write(str(i) + '\n')

    main()