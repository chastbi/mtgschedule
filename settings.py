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