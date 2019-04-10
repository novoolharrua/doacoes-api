
import datetime

periods_enum = {
    'M': {
        'start': '6:00:00',
        'stop': '12:00:00'
    },
    'T': {
        'start': '12:00:00',
        'stop': '18:00:00'
    },
    'N': {
        'start': '18:00:00',
        'stop': '24:00:00'
    }
}

format = '%Y-%m-%d %H:%M:%S'
format_google = '%Y-%m-%dT%H:%M:%S'

def date_to_string(date):
    return date.strftime(format)

def date_to_google(date):
    return date.strftime(format_google)

def format_date_from_period(date, period):

    times = periods_enum.get(period, 'Invalid month')

    start = '{} {}'.format(date, times['start'])
    start = datetime.datetime.strptime(start, format)
    stop = '{} {}'.format(date, times['stop'])
    stop = datetime.datetime.strptime(stop, format)

    return start, stop