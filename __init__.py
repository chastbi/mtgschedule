from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object('settings')
db = SQLAlchemy(app)

# Migrations
migrate = Migrate(app, db)
from mtgschedule.models import Presenter, Schedule

from mtgschedule import views

