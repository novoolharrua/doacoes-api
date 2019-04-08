
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_service():
    from google.oauth2 import service_account

    SCOPES = ['https://www.googleapis.com/auth/calendar']
    SERVICE_ACCOUNT_FILE = 'credencial_sam.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
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
        'summary': '{} calendar for {} region'.format(type, region_name),
        'timeZone': 'America/Sao_Paulo'
    }
    service = get_service()
    created_calendar = service.calendars().insert(body=calendar).execute()

    return created_calendar['id']

def delete_calendar(gcloud_id):
    service = get_service()
    try:
        service.calendars().delete(calendarId=gcloud_id).execute()
        return True
    except HttpError:
        return False

#### EVENTS

def create_event():
    service = get_service()
    event = {
        'summary': 'EVENTAO DA PORRA',
        'location': 'Rodoviaria',
        'description': 'aehooooooooooo',
        'start': {
            'dateTime': '2019-04-03T06:00:00',
            'timeZone': 'America/Sao_Paulo',
        },
        'end': {
            'dateTime': '2019-04-03T12:00:00',
            'timeZone': 'America/Sao_Paulo',
        }
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    print ('Event created: %s' % (event.get('htmlLink')))



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
