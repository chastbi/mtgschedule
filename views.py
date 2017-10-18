from mtgschedule import app, db
from flask import render_template, url_for, redirect, flash, request, session
from mtgschedule.settings import NEW_MRF_URL
from mtgschedule.forms import MeetingForm, AddPresenter
from mtgschedule.models import Schedule, Presenter
from mtgschedule.functions import get_presenters, get_schedule, get_month_events, presenters_available, cities_available,\
    presenter_dictionary, status_count
from mtgschedule.cal_functions import get_weekcal, monthdates_cal, monthsday1_list
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
            selectpresenter = Presenter.query.filter_by(name=request.values['presenter']).first()
            form = MeetingForm(mtg_date=submitdate, presenter=selectpresenter)
        else:
            form = MeetingForm(mtg_date=submitdate)
        error = None
    else:
        form = MeetingForm()
        error = None

    if form.validate_on_submit():
        '''
        edits existing calendar events
        '''
        if request.form.get('mtgid') != "None":
            event = Schedule.query.filter_by(id=request.form.get('mtgid')).first()
            if form.presenter.data:
                event.presenter = form.presenter.data.id
            else:
                event.presenter = None
            event.event = form.event.data
            event.status = form.status.data
            event.mtg_date = form.mtg_date.data
            event.city = form.city.data
            event.state = form.state.data
            event.mtg_time = form.mtg_time1.data
            event.mtg_time2 = form.mtg_time2.data
            event.mtg_topic1 = form.mtg_topic1.data
            event.mtg_topic2 = form.mtg_topic2.data
            event.notes = form.notes.data
            db.session.flush()
            db.session.commit()

            if session['lastdate']:
                return redirect(url_for('wklyschedule') + "/" + session['lastdate'])
            else:
                return redirect(url_for('wklyschedule'))
        '''
        creates new calendar events
        '''
        if form.presenter.data:
            presenterid = form.presenter.data.id
        else:
            presenterid = None
        event = Schedule(
            presenterid,
            form.event.data,
            form.status.data,
            form.mtg_date.data,
            form.city.data,
            form.state.data,
            form.mtg_time1.data,
            form.mtg_time2.data,
            form.mtg_topic1.data,
            form.mtg_topic2.data,
            form.notes.data,
        )
        db.session.add(event)
        db.session.flush()
        db.session.commit()
        flash('Calendar entry submitted.')
        if session['lastdate']:
            return redirect(url_for('wklyschedule') + "/" + session['lastdate'])
        else:
            return redirect(url_for('wklyschedule'))

    return render_template("submitform.html", form=form, error=error)


@app.route('/editevent')
def edit_event():
    id = request.args.get('id')
    event = Schedule.query.filter_by(id=id).first()
    presentername = Presenter.query.filter_by(id=event.presenter).first()

    form = MeetingForm(event=event.event, mtg_date=event.mtg_date, status=event.status, presenter=presentername,
                       city=event.city, state=event.state, mtg_time1=event.mtg_time1, mtg_time2=event.mtg_time2,
                       mtg_topic1=event.mtg_topic1, mtg_topic2=event.mtg_topic2, notes=event.notes)
    error = None
    return render_template("submitform.html", form=form, error=error)


@app.route('/wklyschedule')
@app.route('/wklyschedule/<date>')
def wklyschedule(date=None):
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
    presenters = get_presenters()
    weekcal = get_weekcal(yr, m, finddate)
    schedule_dict = get_schedule(weekcal, "Cancelled")

    return render_template("wklyschedule.html", weekcal=weekcal, presenters=presenters,
                           events=schedule_dict, nextwk=nextwk, lastwk=lastwk, nextmonth=nextmonth, lastmonth=lastmonth,
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
    schedule_dict = get_month_events(monthdates,"Cancelled")
    available_presenters = presenters_available(schedule_dict, monthdates)
    available_cities = cities_available(schedule_dict, monthdates)
    return render_template("pubcal.html", monthdates=monthdates, presenters_avail=available_presenters,
                           cities=available_cities, month_name=month_name, monthlinks=monthlinks, mrf_url=NEW_MRF_URL)


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
    presenters = presenter_dictionary(get_presenters())
    monthdates = monthdates_cal(yr, m)
    complete_mnth_schedule = get_month_events(monthdates)
    if request.args.get('status'):
        status = request.args.get('status')
        schedule_dict = get_month_events(monthdates, status=status)
    else:
        schedule_dict = complete_mnth_schedule

    complete_mnth_schedule = get_month_events(monthdates)
    statuscount = status_count(complete_mnth_schedule)

    monthlinks = monthsday1_list()

    return render_template("eventslist.html", monthdates=monthdates, nextmonth=nextmonth, monthlinks=monthlinks,
                           month_name=month_name, lastmonth=lastmonth, schedule_dict=schedule_dict, presenters=presenters,
                           statuscount=statuscount)


@app.route('/admin')
def admin():
    presenters = get_presenters()
    return render_template("admin.html", presenters=presenters)


@app.route('/mtginfo')
def mtg_info():
    presenters = presenter_dictionary(get_presenters())
    mtg_id = request.args.get('mtgid')
    mrf = Schedule.query.filter_by(id=mtg_id).first()
    return render_template('mtginfo.html', mrf=mrf, presenter=presenters)


@app.route('/delevent')
def delete_event():
    mtgid = request.args.get('id')
    mtg = Schedule.query.filter_by(id=mtgid).first()
    db.session.delete(mtg)
    db.session.flush()
    db.session.commit()
    flash("Meeting Deleted")
    if session['lastdate']:
        return redirect(url_for('wklyschedule') + "/" + session['lastdate'])
    else:
        return redirect(url_for('wklyschedule'))


@app.route('/addpresenter', methods=['GET', 'POST'])
def add_presenter():
    form = AddPresenter()
    error = None

    if form.validate_on_submit():
        presenter = Presenter(form.presenter_name.data)

        db.session.add(presenter)
        db.session.flush()
        db.session.commit()
        flash('Presenter added.')
        return redirect(url_for('wklyschedule'))

    return render_template("addpresenterform.html", form=form, error=error)
