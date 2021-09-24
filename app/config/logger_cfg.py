import os
import platform
import logging
from logging.handlers import TimedRotatingFileHandler
from flask import request

from .base import project_path


class ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.ipaddr = self.get_ip()
        return True

    def get_ip(self):
        try:
            ipaddr = request.remote_addr
        except:
            ipaddr = None
        return ipaddr


def logger():
    formatter = logging.Formatter(
        '[%(ipaddr)s][%(asctime)s][%(pathname)s:%(lineno)d][%(levelname)s] - %(message)s'
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
