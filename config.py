import os

class Config:
    DEBUG = False
    SECRET_KEY = str(os.environ.get('SECRET_KEY'))
    SQLALCHEMY_DATABASE_URI = str(os.environ.get('DATABASE_URL') + os.environ.get('DATABASE_NAME'))

    ADMIN_NAME = str(os.environ.get('ADMIN_NAME'))
    ADMIN_EMAIL = str(os.environ.get('ADMIN_EMAIL'))
    ADMIN_PASSWORD = str(os.environ.get('ADMIN_PASSWORD'))

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
