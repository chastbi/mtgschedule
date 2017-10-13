from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, validators
from wtforms_alchemy import QuerySelectField
from wtforms.fields.html5 import DateField
from mtgschedule.models import Presenter

from datetime import date

class MeetingForm(FlaskForm):
    def get_presenters():
        return Presenter.query.all()

    presenter = QuerySelectField('Presenter', query_factory=lambda: Presenter.query.order_by(Presenter.name).all(),
                                  get_label='name', allow_blank=False)
    event = StringField('Client or Event')
    mtg_date = DateField('Date', format='%Y-%m-%d', default=date.today())
    status = SelectField('Status', choices=[('', ''), ('Requested', 'Requested'), ('Date Reserved', 'Date Reserved'),
                                            ('Ready to Confirm', 'Ready to Confirm'), ('Confirmed', 'Confirmed'),
                                            ('Canceled', 'Canceled')])
    city = StringField('City')
    state = SelectField('State', choices=[('', ''), ('AL', 'AL'), ('AK', 'AK'), ('AZ', 'AZ'), ('AR', 'AR'),
                                        ('CA', 'CA'), ('CO', 'CO'), ('CT', 'CT'), ('DE', 'DE'), ('FL', 'FL'),
                                        ('GA', 'GA'), ('HI', 'HI'), ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'),
                                        ('IA', 'IA'), ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('MN', 'MN'), ('MD', 'MD'),
                                        ('MA', 'MA'), ('MI', 'MI'), ('MN', 'MN'), ('MS', 'MS'), ('MO', 'MO'), ('MT', 'MT'),
                                        ('NE', 'NE'),('NV', 'NV'), ('NH', 'NH'), ('NJ', 'NJ'), ('NM', 'NM'), ('NY', 'NY'),
                                        ('NC', 'NC'),('ND', 'ND'), ('OH', 'OH'), ('OK', 'OK'), ('OR', 'OR'), ('PA', 'PA'),
                                        ('RI', 'RI'), ('SC', 'SC'), ('SD', 'SD'), ('TN', 'TN'), ('TX', 'TX'), ('UT', 'UT'),
                                        ('VT', 'VT'), ('VA', 'VA'), ('WA', 'WA'), ('WV', 'WV'), ('WI', 'WI'), ('WY', 'WY'),])
    mtg_time1 = StringField('1st Mtg Time', [validators.optional()])
    mtg_time2 = StringField('2nd Mtg Time', [validators.optional()])
    mtg_topic1 = StringField('Topic1')
    mtg_topic2 = StringField('Topic2')
    notes = StringField('Notes')


class AddPresenter(FlaskForm):
    presenter_name = StringField('Name', [validators.length(2, 30), validators.DataRequired()])