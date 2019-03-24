import requests
import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime
import json

api_key = os.environ['API_KEY']

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_service():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
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
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


#### CALENDAR

def get_calendar_by_id(calendar_id):
    service = get_service()
    calendar = service.calendars().get(calendarId=calendar_id).execute()

    return calendar

def list_calendars():
    service = get_service()
    result = []
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            result.append(calendar_list_entry)
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    return result

def new_calendar(summary):              #TODO: fix auth
    calendar = {
        'summary': 'calendarSummary',
        'timeZone': 'America/Los_Angeles'
    }
    service = get_service()
    created_calendar = service.calendars().insert(body=calendar).execute()

    print (created_calendar['id'])




#### EVENTS


def get_events_by_calendar_id(calendar_id):
    service = get_service()
    page_token = None
    while True:
        events = service.events().list(calendarId='primary', pageToken=page_token).execute()
        for event in events['items']:
            print(event)
        page_token = events.get('nextPageToken')
        if not page_token:
            break

