from mtgschedule import app, db
from flask import render_template, url_for, redirect, flash, request, session
from mtgschedule.settings import NEW_MRF_URL, MRFS_URL, PRESENTERS, SCHEDULER_LOGIN, PRESENTER_LOGIN
from mtgschedule.decorators import login_required
from mtgschedule.forms import MeetingForm, LoginForm
from mtgschedule.models import Notes
from mtgschedule.functions import get_schedule # presenter_dictionary, status_count,
from mtgschedule.xml_functions import create_mrf_dict
from mtgschedule.cal_functions import get_weekcal, monthdates_cal, monthsday1_list
from mtgschedule.pubcal_functions import available_presenters, cities_available
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from calendar import month_name


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/submitform', methods=['GET', 'POST'])
def submitform():
    if request.method == 'GET' and request.args.get('submitdate'):
        '''
        if page accessed from calendar, sets up prefill of presenter name and date
        '''
        submitdate = datetime.strptime(request.values['submitdate'], "%Y-%m-%d")
        submitdate = submitdate.date()
        if request.args.get('presenter'):
            selectpresenter = request.args.get('presenter')
            form = MeetingForm(date=submitdate, presenter=selectpresenter)
        else:
            form = MeetingForm(date=submitdate)
        error = None
    else:
        form = MeetingForm()
        error = None

    if form.validate_on_submit():
        '''
        edits existing schedule notes
        '''
        if request.form.get('noteid') != "None":
            note = Notes.query.filter_by(id=request.form.get('noteid')).first()
            note.presenter = form.presenter.data
            note.date = form.date.data
            note.notes = form.notes.data
            db.session.flush()
            db.session.commit()

            if session['lastdate']:
                return redirect(url_for('wklyschedule') + "/" + session['lastdate'])
            else:
                return redirect(url_for('wklyschedule'))
        '''
        creates new schedule notes
        '''
        note = Notes(
            form.presenter.data,
            form.date.data,
            form.notes.data,
        )
        db.session.add(note)
        db.session.flush()
        db.session.commit()
        flash('Scheduler note submitted.')
        if session['lastdate']:
            return redirect(url_for('wklyschedule') + "/" + session['lastdate'])
        else:
            return redirect(url_for('wklyschedule'))

    return render_template("submitform.html", form=form, error=error)


@app.route('/wklyschedule')
@app.route('/wklyschedule/<date>')
@login_required
def wklyschedule(date=None):
    '''
    navigation
    '''
    session['lastdate'] = None
    if date:
        finddate = datetime.strptime(date, "%Y-%m-%d")
        session['lastdate'] = date
    else:
        finddate = datetime.today() + timedelta(days=90)
    yr = finddate.year
    m = finddate.month
    nextweek = finddate + timedelta(days=7)
    nextwk = nextweek.date()
    lastweek = finddate - timedelta(days=7)
    lastwk = lastweek.date()
    weeks = monthdates_cal(yr, m)
    monthlinks = monthsday1_list()

    '''
    calendar creation
    '''
    weekcal = get_weekcal(yr, m, finddate)
    '''
    load meetings
    '''
    mrfs = create_mrf_dict() #xml
    notes = get_schedule(weekcal)
    return render_template("wklyschedule.html", weekcal=weekcal, presenters=PRESENTERS, notes=notes,
                           nextwk=nextwk, lastwk=lastwk, monthlinks=monthlinks, month_name=month_name, weeks=weeks,
                           lastdate=session['lastdate'], mrfs=mrfs, mrfs_url=MRFS_URL)


@app.route('/webinarschedule')
@app.route('/webinarschedule/<date>')
@login_required
def webinarschedule(date=None):
    session['lastdate'] = None
    if date:
        finddate = datetime.strptime(date, "%Y-%m-%d")
        session['lastdate'] = date
    else:
        finddate = datetime.today() + timedelta(days=90)
    yr = finddate.year
    m = finddate.month
    nextweek = finddate + timedelta(days=7)
    nextwk = nextweek.date()
    lastweek = finddate - timedelta(days=7)
    lastwk = lastweek.date()
    nextmnth = finddate + relativedelta(months=1)
    nextmonth = nextmnth.date()
    lastmnth = finddate - relativedelta(months=1)
    lastmonth = lastmnth.date()

    weeks = monthdates_cal(yr, m)
    monthlinks = monthsday1_list()
    weekcal = get_weekcal(yr, m, finddate)

    roomlist = ["PA Main", "PA #2", "AZ Main", "AZ #2"]

    return render_template("webinarcalendar.html", weekcal=weekcal, roomlist=roomlist,
                           nextwk=nextwk, lastwk=lastwk, nextmonth=nextmonth, lastmonth=lastmonth,
                           monthlinks = monthlinks, month_name=month_name, weeks=weeks, lastdate=session['lastdate'])


@app.route('/pubcal')
@app.route('/pubcal/<date>')
def pubcal(date=None):
    if date:
        finddate = datetime.strptime(date, "%Y-%m-%d")
    else:
        finddate = datetime.today() + timedelta(days=90)
    yr = finddate.year
    m = finddate.month

    monthlinks = monthsday1_list()
    monthdates = monthdates_cal(yr, m)

    availability = available_presenters(monthdates) #xml
    cities = cities_available(monthdates)

    return render_template("pubcal.html", monthdates=monthdates, availability=availability, cities=cities,
                           month_name=month_name, monthlinks=monthlinks, mrf_url=NEW_MRF_URL)

'''
@app.route('/eventslist')
@app.route('/eventslist/<date>')
def eventslist(date=None):
    if date:
        finddate = datetime.strptime(date, "%Y-%m-%d")
    else:
        finddate = datetime.today() + timedelta(days=90)
    yr = finddate.year
    m = finddate.month

    nextmnth = finddate + timedelta(days=28)
    nextmonth = nextmnth.date()
    lastmnth = finddate - timedelta(days=28)
    lastmonth = lastmnth.date()
    monthlinks = monthsday1_list()
    presenters = presenter_dictionary(get_presenters())
    monthdates = monthdates_cal(yr, m)
    complete_mnth_schedule = get_month_events(monthdates)
    statuscount = status_count(complete_mnth_schedule)

    if request.args.get('status'):
        status = request.args.get('status')
        schedule_dict = get_month_events(monthdates, status=status)
    else:
        schedule_dict = complete_mnth_schedule
    return render_template("eventslist.html", monthdates=monthdates, nextmonth=nextmonth, monthlinks=monthlinks,
                           month_name=month_name, lastmonth=lastmonth, schedule_dict=schedule_dict, presenters=presenters,
                           statuscount=statuscount)
'''


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        if form.username.data == SCHEDULER_LOGIN['username'] and form.password.data == SCHEDULER_LOGIN['password']:
            session['username'] = form.username.data
            return redirect(url_for('wklyschedule'))
        elif form.username.data == PRESENTER_LOGIN['username'] and form.password.data == PRESENTER_LOGIN['password']:
            session['username'] = form.username.data
            return redirect(url_for('wklyschedule'))
        else:
            error = "Incorrect username and password."
    return render_template("login.html", form=form, error=error)


@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop('username')
    return redirect(url_for('index'))


@app.route('/noteinfo')
def note_info():
    noteid = request.args.get('noteid')
    note = Notes.query.filter_by(id=noteid).first()
    note = note.notes_dict
    return render_template('mtginfo.html', note=note)


@app.route('/editnote')
def editnote():
    noteid = request.args.get('noteid')
    note = Notes.query.filter_by(id=noteid).first()

    form = MeetingForm(date=note.date, presenter=note.presenter, notes=note.notes)
    error = None
    return render_template("submitform.html", form=form, error=error)


@app.route('/delnote')
def delete_note():
    noteid = request.args.get('noteid')
    note = Notes.query.filter_by(id=noteid).first()
    db.session.delete(note)
    db.session.flush()
    db.session.commit()
    flash("Scheduler note deleted")
    if session['lastdate']:
        return redirect(url_for('wklyschedule') + "/" + session['lastdate'])
    else:
        return redirect(url_for('wklyschedule'))
