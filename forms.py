from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators
from wtforms.fields.html5 import DateField
from mtgschedule.settings import PRESENTERS_LIST

from datetime import date


class MeetingForm(FlaskForm):
    presenter = SelectField('Presenter', choices=[name for name in PRESENTERS_LIST])
    date = DateField('Date', format='%Y-%m-%d', default=date.today())
    notes = StringField('Notes')


class AddPresenter(FlaskForm):
    presenter_name = StringField('Name', [validators.length(2, 30), validators.DataRequired()])