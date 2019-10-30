import datetime

DATE_FORMAT = '%Y-%m-%d'

def today():
    return datetime.datetime.today().strftime(DATE_FORMAT)

def date_object(date):
    return datetime.datetime.strptime(date, DATE_FORMAT)
