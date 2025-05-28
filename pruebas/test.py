import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
      # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("calendar", "v3", credentials=creds)
        acl = service.acl().list(calendarId='ade6f94727398819179a36bf79ecc88689ea39a9c0e07ca646b6f747c36febaa@group.calendar.google.com').execute()
        print("PUBLICO")
        for rule in acl['items']:
            print('%s: %s' % (rule['id'], rule['role']))
        
        acl = service.acl().list(calendarId='79c7256a4968ade9ef7b36acbe3e331c0a8d0c528ac0cd3cb93bba06179a4e3b@group.calendar.google.com').execute()
        print("PRIVADO")
        for rule in acl['items']:
            print('%s: %s' % (rule['id'], rule['role']))

        rule = {
            'scope': {
                'type': 'default',
            },
            'role': 'reader'
        }
        acl = service.acl().insert(calendarId='79c7256a4968ade9ef7b36acbe3e331c0a8d0c528ac0cd3cb93bba06179a4e3b@group.calendar.google.com',body=rule).execute()
    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
