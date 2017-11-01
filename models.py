from mtgschedule import db


class Notes(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    presenter = db.Column(db.String(60))
    date = db.Column(db.Date)
    notes = db.Column(db.String(240))

    def __init__(self, presenter, date, notes):
        self.presenter = presenter
        self.date = date
        self.notes = notes

    @property
    def notes_dict(self):
        return {'id': self.id, 'date': self.date, 'presenter': self.presenter, 'notes': self.notes}
