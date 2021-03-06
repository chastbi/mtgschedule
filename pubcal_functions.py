from mtgschedule.settings import PRESENTERS, RUSH_TIMEFRIME
from mtgschedule.xml_functions import create_mrf_dict
from mtgschedule.sql_functions import get_month_notes
from datetime import timedelta, date


def presenter_mtg_days(mrflist):
    '''
    create presenter mtg day dictionary names are keys. value is list of busy days for the presenter based on mrf data
    :return {'Brad Chastain': [datetime.date(2018, 1, 24)], 'Dennis Hale': [datetime.date(2018, 1, 24)],
              'Steve Roberts': [datetime.date(2018, 1, 24), datetime.date(2018, 1, 23)],
    '''
    mtg_days = {}

    for presenter in PRESENTERS:
        mtg_days[presenter['name']] = []

    for mrf, values in mrflist.items():
        if values['status'] != 'Cancelled' and values['type'] != 'Webinar':
            try:
                mtg_days[values['presenter1']].append(values['date'])
            except:
                pass
            try:
                mtg_days[values['presenter2']].append(values['date'])
            except:
                pass
            try:
                mtg_days[values['presenter3']].append(values['date'])
            except:
                pass
            try:
                mtg_days[values['presenter4']].append(values['date'])
            except:
                pass
    return mtg_days


def notes_days(cal):
    busy_days = {}
    notes = get_month_notes(cal)
    for presenter in PRESENTERS:
        busy_days[presenter['name']] = []
    for note in notes:
        today = note['date']
        tomorrow = today + timedelta(days=1)
        if today not in busy_days[note['presenter']]:
            busy_days[note['presenter']].append(today)
        if tomorrow not in busy_days[note['presenter']]:
            busy_days[note['presenter']].append(tomorrow)
    return busy_days


def available_presenters(cal):
    # returns a dictionary of dates(strings) and number of available presenters for that day.

    available_count = {}
    qty_presenters = len(PRESENTERS)

    mrflist = create_mrf_dict()
    mtg_days = presenter_mtg_days(mrflist)
    for mrf, values in mrflist.items():
        if values['status'] != 'Cancelled':
            today = values['date']
            tomorrow = today + timedelta(days=1)
            yesterday = today - timedelta(days=1)
            for presenter, dates in mtg_days.items():
                if tomorrow not in mtg_days[presenter]:
                    if values['presenter1'] == presenter or values['presenter2'] == presenter:
                        mtg_days[presenter].append(tomorrow)
                if yesterday not in mtg_days[presenter]:
                    if values['presenter1'] == presenter or values['presenter2'] == presenter:
                        mtg_days[presenter].append(yesterday)

    notes = get_month_notes(cal)
    for note in notes:
        today = note['date']
        tomorrow = today + timedelta(days=1)
        if today not in mtg_days[note['presenter']]:
            mtg_days[note['presenter']].append(today)
        if tomorrow not in mtg_days[note['presenter']]:
            mtg_days[note['presenter']].append(tomorrow)

    for week in cal:
        for day in week:
            if day < date.today() + timedelta(days=RUSH_TIMEFRIME):
                available_count[day] = 0
            else:
                available_count[day] = qty_presenters
    for presenter, days in mtg_days.items():
        for day in days:
            # below if could be deleted if only mrf within the cal range is provided
            if day in available_count.keys() and day.weekday() != 5:  # prevents errors when not in range of month
                available_count[day] -= 1

    return available_count


def cities_available(cal):
    '''
    creates a dictionary of cities where we might be able to do meetings. datetime object is key, cities are values
    '''
    available_cities = {}
    mrflist = create_mrf_dict()
    mtg_days = presenter_mtg_days(mrflist)
    for week in cal:
        for day in week:
            available_cities[day] = []

    for mrf, values in mrflist.items():
        if values['status'] != 'Cancelled':
            presenters = []
            if values['presenter1']:
                presenters.append(values['presenter1'])
            if values['presenter2']:
                presenters.append(values['presenter2'])
            if values['presenter3']:
                presenters.append(values['presenter3'])
            if values['presenter4']:
                presenters.append(values['presenter4'])
            city = values['city']
            state = values['state']
            location = city + ", " + state
            day = values['date']
            dayafter = day + timedelta(days=1)
            day2after = day + timedelta(days=2)
            daybefore = day - timedelta(days=1)
            day2before = day - timedelta(days=2)

            note_days = notes_days(cal)

            for presenter in presenters:
                if dayafter not in mtg_days[presenter] and day2after not in mtg_days[presenter] and values['city'] != ''\
                        and dayafter not in note_days[presenter] and day >= date.today() + timedelta(days=RUSH_TIMEFRIME):
                    # below if could be deleted if only mrf within the cal range is provided
                    if dayafter in available_cities.keys() and location not in available_cities[dayafter]:
                        available_cities[dayafter].append(location)
                if daybefore not in mtg_days[presenter] and day2before not in mtg_days[presenter] and values['city'] != ''\
                        and daybefore not in note_days[presenter] and day >= date.today() + timedelta(days=RUSH_TIMEFRIME):
                    # below if could be deleted if only mrf within the cal range is provided
                    if daybefore in available_cities.keys() and location not in available_cities[daybefore]:
                        available_cities[daybefore].append(location)

    return available_cities
