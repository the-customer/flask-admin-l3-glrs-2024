import os

DEBUG=1

APP_NAME = "EBC"

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir,"data.db")

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "HereIsMySecretKey"

NO_IMG = "https://t4.ftcdn.net/jpg/04/73/25/49/360_F_473254957_bxG9yf4ly7OBO5I0O5KABlN930GwaMQz.jpg"