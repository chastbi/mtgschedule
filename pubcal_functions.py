from mtgschedule.settings import PRESENTERS
from mtgschedule.xml_functions import create_mrf_dict
from datetime import timedelta, date


def presenter_mtg_days(mrflist):
    # create presenter mtg day dictionary names are keys. value is list of busy days for the presenter based on mrf data

    mtg_days = {}

    for presenter in PRESENTERS:
        mtg_days[presenter['name']] = []
    '''
    for mrf, values in mrflist.items():
        today = values['date']
        tomorrow = values['date'] + timedelta(days=1)  #this stuff needs moved to available presenters
        yesterday = values['date'] - timedelta(days=1)
        if today not in mtg_days[values['presenter1']]:
            mtg_days[values['presenter1']].append(today)
        if tomorrow not in mtg_days[values['presenter1']]:
            mtg_days[values['presenter1']].append(tomorrow)
        if yesterday not in mtg_days[values['presenter1']]:
            mtg_days[values['presenter1']].append(yesterday)'''

    for mrf, values in mrflist.items():
        mtg_days[values['presenter1']].append(values['date'])
    return mtg_days


def available_presenters(cal):
    # returns a dictionary of dates(strings) and number of available presenters for that day.

    available_count = {}
    qty_presenters = len(PRESENTERS)
    mrflist = create_mrf_dict()
    mtg_days = presenter_mtg_days(mrflist)

    for week in cal:
        for day in week:
            available_count[day] = qty_presenters
    for presenter, days in mtg_days.items():
        for day in days:
            # below if could be deleted if only mrf within the cal range is provided
            if day in available_count.keys():
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
        if values['presenter1']:
            print("PREENTERS FOUND")
            presenter1 = values['presenter1']
            city = values['city']
            state = values['state']
            location = city + ", " + state
            day = values['date']
            dayafter = day + timedelta(days=1)
            day2after = day + timedelta(days=2)
            daybefore = day - timedelta(days=1)
            day2before = day - timedelta(days=2)
            print(mtg_days)
            if dayafter not in mtg_days[presenter1] and day2after not in mtg_days.keys() and \
                            dayafter >= date.today() + timedelta(days=31) and values['city'] != '':
                # below if could be deleted if only mrf within the cal range is provided
                if dayafter in available_cities.keys():
                    available_cities[dayafter].append(location)
            if daybefore not in mtg_days[presenter1] and day2before not in mtg_days.keys() and \
                            dayafter >= date.today() + timedelta(days=31) and values['city'] != '':
                # below if could be deleted if only mrf within the cal range is provided
                if daybefore in available_cities.keys():
                    available_cities[daybefore].append(location)

    return available_cities
