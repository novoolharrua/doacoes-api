
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils.name_utils import translate_name
import os
from base64 import b64decode
import json

SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_service():
    from google.oauth2 import service_account

    json_base64 = os.environ['BASE64_CREDENTIALS']
    info = json.loads(b64decode(json_base64).decode('utf-8'))
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    SERVICE_ACCOUNT_FILE = 'credencial_sam.json'

    credentials = service_account.Credentials.from_service_account_info(
        info, scopes=SCOPES)
    delegated_credentials = credentials.with_subject('lucas@necconstrucoes.com')
    service = build('calendar', 'v3', credentials=delegated_credentials)
    return service

#### CALENDAR

def get_calendar_by_id(calendar_id):
    service = get_service()
    calendar = service.calendars().get(calendarId=calendar_id).execute()

    return calendar

def create_calendar(region_name, type):
    calendar = {
        'summary': '{} - {}'.format(region_name, translate_name(type.upper())),
        'timeZone': 'America/Sao_Paulo'
    }
    service = get_service()
    created_calendar = service.calendars().insert(body=calendar).execute()
    rule = {
        "role": "reader",
        "scope": {
            "type": "default"
    }
}
    service.acl().insert(calendarId=created_calendar['id'], body=rule).execute()

    return created_calendar['id']

def delete_calendar(gcloud_id):
    service = get_service()
    try:
        service.calendars().delete(calendarId=gcloud_id).execute()
        return True
    except HttpError:
        return False

#### EVENTS


def post_event(region, calendar, institution, donation_type, start, stop):
    service = get_service()
    event = {
        'summary': '{}'.format(institution.name),
        'location': region.address,
        'description': 'Doação de {} para o grupo {}'.format(translate_name(donation_type), region.name),
        'start': {
            'dateTime': start,
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': stop,
            'timeZone': 'America/Sao_Paulo',
        },
        'attendees': []
    }

    event = service.events().insert(calendarId=calendar.gcloud_id, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
    return event


def delete_event(calendar_id, event_id):
    service = get_service()
    service.events().delete(calendarId=calendar_id, eventId=event_id).execute()


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
