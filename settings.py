import os

SECRET_KEY = 'hard to guess key'
DEBUG = True
DB_USERNAME = 'root'
DB_PASSWORD = 'root'
BLOG_DATABASE_NAME = 'meetingsgroup'
DB_HOST = 'localhost'
DB_URI = "mysql+pymysql://%s:%s@%s/%s" % (DB_USERNAME, DB_PASSWORD, DB_HOST, BLOG_DATABASE_NAME)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
NEW_MRF_URL="http://iigsp.vanguard.com/irps/pex/_layouts/FormServer.aspx?XsnLocation=/irps/pex/pemeeting/" \
            "MeetingRequestForms/Forms/template.xsn&SaveLocation=http://iigsp.vanguard.com/irps/pex/pemeeting/" \
            "MeetingRequestForms&ClientInstalled=true&Source=http://iigsp.vanguard.com/irps/pex/pemeeting/pages/" \
            "Home.aspx&OpenIn=Client"
MRF_LIST="./mrfs/"

PRESENTERS=[{'name':'Brad Chastain', 'site':'AZ'},
            {'name':'Dennis Hale', 'site':'AZ'},
            {'name':'Steve Roberts', 'site':'AZ'},
            {'name':'Andrew Crouch', 'site':'PA'}]
