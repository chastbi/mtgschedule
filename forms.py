from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField
from mtgschedule.settings import PRESENTERS_LIST

from datetime import date


class MeetingForm(FlaskForm):
    presenter = SelectField('Presenter', choices=[name for name in PRESENTERS_LIST], validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', default=date.today(), validators=[DataRequired()])
    notes = StringField('Notes', validators=[DataRequired()])


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')