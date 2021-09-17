import os
import datetime
import platform
import logging
from logging.handlers import TimedRotatingFileHandler

from .base import project_path


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


def logger():
    formatter = logging.Formatter(
        '[%(asctime)s][%(pathname)s:%(lineno)d][%(levelname)s] - %(message)s'
    )
    file_dir = os.path.join(project_path, 'app', 'logs')
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    file_name = os.path.join(file_dir, 'flask.log')
    if platform.system() == 'Linux':
        handler = TimedRotatingFileHandler(file_name, when='D', interval=1, backupCount=15,
                                           encoding='UTF-8', delay=False, utc=True)
    else:
        handler = logging.FileHandler(file_name)

    handler.setFormatter(formatter)
    return handler


logger = logger()
