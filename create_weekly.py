from calendar import Calendar

cal = Calendar(firstweekday=6)


def monthdates_cal(yr, m):
    '''
    creates a 1 month list of weeks where the days are datetime.date objects
    :param yr: year
    :param m: month
    :return: [datetime.date(2017-10-25), ...][.....]
    '''
    monthdates = cal.monthdatescalendar(yr, m)
    return monthdates


# returns the week of days as datetime.date objects containing the search date from a larger calendar
def weekdates_cal(monthcal, finddate):
    '''
    creates a 1 week list of days (datetime.date objects) of the week containing the finddate. Sun-Sat of the week
    :param monthcal: takes in a Calendar.monthdatescalendar list
    :param finddate: the date that is within the week which is to be returned. format yyyy-mm-d
    :return: [datetime.date(2017-10-25), ...][.....]
    '''
    calweek = []
    for week in monthcal:
        if finddate in week:
            for day in week:
                calweek.append(day)
    return calweek
