from mtgschedule import app, db
from flask import render_template, url_for, redirect, flash, request
from mtgschedule.forms import MeetingForm, AddPresenter
from mtgschedule.models import Schedule, Presenter
from mtgschedule.functions import get_presenters, get_schedule, get_month_events, presenters_available, cities_available
from mtgschedule.cal_functions import get_weekcal, monthdates_cal, monthsday1_list
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from calendar import month_name


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/submitform', methods=['GET', 'POST'])
def submitform():
    if request.method == 'GET' and request.args.get('presenter'):
        submitdate = datetime.strptime(request.values['submitdate'], "%Y-%m-%d")
        submitdate = submitdate.date()
        selectpresenter = Presenter.query.filter_by(name=request.values['presenter']).first()
        form = MeetingForm(mtg_date=submitdate, presenter=selectpresenter)
        error = None
    else:
        form = MeetingForm()
        error = None

    if form.validate_on_submit():
        event = Schedule(
            form.presenter.data.id,
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
        return redirect(url_for('wklyschedule'))


    return render_template("submitform.html", form=form, error=error)


@app.route('/wklyschedule')
@app.route('/wklyschedule/<date>')
def wklyschedule(date=None):
    if date:
        finddate = datetime.strptime(date, "%Y-%m-%d")
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
    schedule_dict = get_schedule(weekcal)
    return render_template("wklyschedule.html", weekcal=weekcal, presenters=presenters,
                           events=schedule_dict, nextwk=nextwk, lastwk=lastwk, nextmonth=nextmonth, lastmonth=lastmonth,
                           monthlinks = monthlinks, month_name=month_name, weeks=weeks)


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
    schedule_dict = get_month_events(monthdates)
    available_presenters = presenters_available(schedule_dict, monthdates)
    available_cities = cities_available(schedule_dict, monthdates)
    return render_template("pubcal.html", monthdates=monthdates, presenters_avail=available_presenters,
                           cities=available_cities, month_name=month_name, monthlinks=monthlinks)


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
    presenters = get_presenters()
    monthdates = monthdates_cal(yr, m)
    schedule_dict = get_month_events(monthdates)
    return render_template("eventslist.html", monthdates=monthdates, nextmonth=nextmonth,
                           lastmonth=lastmonth, schedule_dict=schedule_dict, presenters=presenters)


@app.route('/admin')
def admin():
    presenters = get_presenters()
    return render_template("admin.html", presenters=presenters)


@app.route('/mtginfo')
def mtg_info():
    mtg_id = request.args.get('mtgid')
    mrf = Schedule.query.filter_by(id=mtg_id).first()
    return render_template('mtginfo.html', mrf=mrf)

@app.route('/editform')
def edit_form():
    return "Edit Form"

@app.route('/deletemtg')
def delete_mtg():
    mtgid = request.args.get('id')
    mtg = Schedule.query.filter_by(id=mtgid).first()
    db.session.delete(mtg)
    db.session.flush()
    db.session.commit()
    flash("Meeting Deleted")
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
