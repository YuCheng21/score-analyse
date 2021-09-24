import os
import platform
import logging
from logging.handlers import TimedRotatingFileHandler
from flask import request

from .base import project_path


class RequestFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        record.url = request.url
        record.remote_addr = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
        return super(RequestFormatter, self).format(record=record)


def logger():
    file_dir = os.path.join(project_path, 'app', 'logs')
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    file_name = os.path.join(file_dir, 'flask.log')

    if platform.system() == 'Linux':
        handler = TimedRotatingFileHandler(file_name, when='D', interval=1, backupCount=15,
                                           encoding='UTF-8', delay=False, utc=True)
    else:
        handler = logging.FileHandler(file_name)

    formatter = RequestFormatter(
        fmt='[%(remote_addr)s][%(asctime)s.%(msecs)03d][%(pathname)s:%(lineno)d][%(levelname)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    return handler
