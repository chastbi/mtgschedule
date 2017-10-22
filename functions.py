from mtgschedule.models import Notes
from datetime import date, timedelta

'''
def get_presenters():
    returns a dictionary of presenters from database
    presenters = Presenter.query.order_by(Presenter.name).all()
    presenter_dict = [item.presenter_dict for item in presenters]
    return presenter_dict
'''


def get_schedule(weekcal):
    '''
    returns a dictionary of one week's Notes within that occur within weekcal (used on weekly schedule)
    '''
    notes = Notes.query.filter(Notes.date.between(weekcal[0], weekcal[-1])).all()
    notes_dict = [item.notes_dict for item in notes]
    return notes_dict


def get_month_notes(monthcal):
    '''
    return Notes within a monthcal as a dictionary (used on pubcal.html)
    '''
    firstday = monthcal[0][0]
    lastday = monthcal[-1][-1]
    notes = Notes.query.filter(Notes.date.between(firstday, lastday)).all()
    notes_dict = [item.notes_dict for item in notes]
    return notes_dict


def presenters_available(schedule_dict, monthdates):
    '''
    returns dictionary of monthdates and number of available presenters
    :return:
    '''
    #presenters = get_presenters()
    #presenterqty = len(presenters)
    # create a dictionary of presenters listing busy days (includes travel days)
    unavail = {}
    for presenter in presenters:
        unavail[presenter['name']] = []
    for event in schedule_dict:
        if event['presenter']:
            presenterid = event['presenter']
            presentername = get_presenter_name(presenterid, presenters)
            today = event['mtg_date']
            tomorrow = event['mtg_date'] + timedelta(days=1)
            yesterday = event['mtg_date'] - timedelta(days=1)
            if today not in unavail[presentername]:
                unavail[presentername].append(today)
            if tomorrow not in unavail[presentername]:
                unavail[presentername].append(tomorrow)
            if yesterday not in unavail[presentername]:
                unavail[presentername].append(yesterday)

    '''create dictionary of monthdates with number of presenters available each day.  
    Hides next 31 days of results'''
    avail = {}
    for week in monthdates:
        for day in week:
            if day < date.today() + timedelta(days=31):
                avail[day] = 0
            else:
                avail[day] = presenterqty
    for presenter in unavail:
        for day in unavail[presenter]:
            if day > date.today() + timedelta(days=31) and day.weekday() !=5: # don't subtract from sat to avoid errors since the 1st sat isn't in range
                avail[day] -= 1
    return avail


def _get_city(schedule_dict, day):
    for event in schedule_dict:
        if event['mtg_date'] == day:
            city = event['city']
            return city


def cities_available(schedule_dict, monthdates):
    presenters = get_presenters()
    '''
    creates a dictionary for actual meeting(busy) days. presenter name is key and has list of meeting dates
    '''
    mtgday = {}
    for presenter in presenters:
        mtgday[presenter['name']] = []
    for event in schedule_dict:
        if event['presenter']:
            presenterid = event['presenter']
            presentername = get_presenter_name(presenterid, presenters)
            today = event['mtg_date']

            if today not in mtgday[presentername]:
                mtgday[presentername].append(today)

    '''
    creates dictionary of dates with available cities
    '''
    avail_cities = {}
    for week in monthdates:
        for day in week:
            avail_cities[day] = []
    for event in schedule_dict:
        if event['presenter']:
            presenterid = event['presenter']
            presentername = get_presenter_name(presenterid, presenters)
            city = event['city']
            state = event['state']
            location = city + ", " + state
            day = event['mtg_date']
            dayafter = day + timedelta(days=1)
            day2after = day + timedelta(days=2)
            daybefore = day - timedelta(days=1)
            day2before = day - timedelta(days=2)
            if dayafter not in mtgday[presentername] and day2after not in mtgday[presentername] and \
                            dayafter >= date.today() + timedelta(days=31) and event['city'] != '':
                avail_cities[dayafter].append(location)
            if daybefore not in mtgday[presentername] and day2before not in mtgday[presentername] and \
                            dayafter >= date.today() + timedelta(days=31) and event['city'] != '':
                avail_cities[daybefore].append(location)
    return avail_cities


def get_presenter_name(id, presenters):
    presentername = {}
    '''
    returns a presenter name from presenter dictionary using the id
    '''
    for presenter in presenters:
        if presenter['id'] == id:
            presentername = presenter['name']
    return presentername


def presenter_dictionary(presenters):
    dict = {}
    for presenter in presenters:
        dict[presenter['id']] = presenter['name']
    return dict


def status_count(schedule_dict):
    '''
    create and return a dictionary of items with qty of each item
    '''
    statuscount = {}
    for event in schedule_dict:
        statuscount[event['status']] = 0
    for event in schedule_dict:
        statuscount[event['status']] += 1

    return statuscount