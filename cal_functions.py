from calendar import Calendar
from datetime import datetime, timedelta


def monthdates_cal(yr, m):
    '''
    returns a month's list of weeks with the days as datetime.date objects
    :return: [datetime.date(2017-04-15), ....],[datetime.date(2017-04-22)...]
    '''
    cal = Calendar(firstweekday=6)
    monthdates = cal.monthdatescalendar(yr, m)

    return monthdates


def weekdates_cal(monthdates, finddate):
    '''
    returns the week containing finddate as a list of datetime.date objects. the week is Sun-Sat.
    :param monthdates: from the monthdates_cal function
    :param finddate: a datetime.dates object to search for
    :return: [datetime.date(2017-04-15), ....]
    '''
    for week in monthdates:
        if finddate in week:
            return week
    return "Date not found"


def get_weekcal(yr, m, searchdate):
    '''
    takes a date and searches for the week in which that date occurs
    returns the week as a list of Sun - Sat datetime.date objects.
    '''
    monthdates = monthdates_cal(yr, m)
    finddate = datetime.date(searchdate)

    weekcal = weekdates_cal(monthdates, finddate)
    return weekcal


def monthsday1_list():
    '''
    returns a list of datetime.date objects for the first day of each of the next 12 months
    used for navigation on the presenter weekly schedule
    '''
    now = datetime(datetime.now().year, datetime.now().month, 1)
    oneyear = now + timedelta(days=330)
    months = [now.date()]

    while now <= oneyear:
        now += timedelta(days=32)
        months.append(datetime(now.year, now.month, 1).date())
    return months

