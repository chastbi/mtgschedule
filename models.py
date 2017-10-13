from mtgschedule import db


class Presenter(db.Model):
    __tablename__ = 'presenters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    active = db.Column(db.Boolean)

    presentername = db.relationship('Schedule', backref='presentername', lazy='dynamic')

    def __init__(self, name):
        self.name = name
        self.active = True


    @property
    def presenter_dict(self):
        return {'id': self.id, 'name': self.name, 'active': self.active}

    def __repr__(self):
        return "%r" % self.name


class Schedule(db.Model):
    __tablename__ = 'schedule'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String(80))
    mtg_date = db.Column(db.Date)
    status = db.Column(db.String(20))
    presenter = db.Column(db.Integer, db.ForeignKey('presenters.id'))
    city = db.Column(db.String(30))
    state = db.Column(db.String(2))
    mtg_time1 = db.Column(db.String(10))
    mtg_time2 = db.Column(db.String(10))
    mtg_topic1 = db.Column(db.String(20))
    mtg_topic2 = db.Column(db.String(20))
    notes = db.Column(db.String(120))

    def __init__(self, presenter, event, status='Requested', date=None, city=None, state=None, mtg_time1=None, mtg_time2=None,
                 mtg_topic1=None, mtg_topic2=None, notes=None):
        self.presenter = presenter
        self.event = event
        self.status = status
        self.mtg_date = date
        self.city = city
        self.state = state
        self.mtg_time1 = mtg_time1
        self.mtg_time2 = mtg_time2
        self.mtg_topic1 = mtg_topic1
        self.mtg_topic2 = mtg_topic2
        self.notes = notes

    @property
    def schedule_dict(self):
        return {
            'id' : self.id,
            'presenter' : self.presenter,
            'event' : self.event,
            'status' : self.status,
            'mtg_date' : self.mtg_date,
            'city' : self.city,
            'state' : self.state,
            'mtg_time1' : self.mtg_time1,
            'mtg_time2' : self.mtg_time2,
            'mtg_topic1' : self.mtg_topic1,
            'mtg_topic2' : self.mtg_topic2,
            'notes' : self.notes
        }

    def __repr__(self):
        return "%r, %r" % (self.event, self.presentername)

