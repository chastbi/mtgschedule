import os

SECRET_KEY = 'hard to guess key'
DEBUG = True
DB_USERNAME = 'root'
DB_PASSWORD = 'root'
NOTES_DATABASE_NAME = 'notes'
DB_HOST = 'localhost'
DB_URI = "mysql+pymysql://%s:%s@%s/%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST, NOTES_DATABASE_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
NEW_MRF_URL=""

MRFS_DIRECTORY= "./mrfs/"
MRFS_URL = os.path.abspath(MRFS_DIRECTORY)

PRESENTERS=[{'name':'Brad Chastain', 'site':'AZ'},
            {'name':'Dennis Hale', 'site':'AZ'},
            {'name':'Steve Roberts', 'site':'AZ'},
            {'name':'Andrew Crouch', 'site':'PA'},
            {'name':'Michael Gozdowski', 'site':'PA'},
            {'name':'Lourdes Nieves', 'site':'PA'}]

PRESENTERS_LIST  = [('Andrew Crouch', 'Andrew Crouch'), ('Brad Chastain', 'Brad Chastain'),
                    ('Dennis Hale', 'Dennis Hale'), ('Lourdes Nieves', 'Lourdes Nieves'),
                    ('Michael Gozdowski', 'Michael Gozdowski'), ('Steve Roberts', 'Steve Roberts')]

RUSH_TIMEFRIME = 31

SCHEDULER_LOGIN = {'username': 'scheduler', 'password': 'scheduler'}
PRESENTER_LOGIN = {'username': 'presenter', 'password': 'presenter'}