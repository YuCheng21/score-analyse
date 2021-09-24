import os
import datetime


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JSON_AS_ASCII = False
    SESSION_COOKIE_NAME = 'sa-session'
    SESSION_REFRESH_EACH_REQUEST = True
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=30)


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
