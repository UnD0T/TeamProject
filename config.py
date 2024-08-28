import os
from decouple import config


BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '123456789'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///'+os.path.join(BASEDIR, 'teamproject.db')
    UPLOAD_PATH = os.environ.get('UPLOAD_PATH')