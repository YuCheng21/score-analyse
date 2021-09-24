from flask import Flask, render_template, g
import os

from .config.flask_cfg import config as flask_config
from .config.logger_cfg import logger as log_handler
from .config.logger_cfg import ContextFilter as LogFilter
from .config.base import project_path, website_name

from .view.root import app as root


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(flask_config[config_name])
    app.static_folder = os.path.join(project_path, 'app', 'static')
    app.template_folder = os.path.join(project_path, 'app', 'templates')

    app.register_blueprint(root)

    app.logger.addHandler(log_handler())
    app.logger.addFilter(LogFilter())

    @app.before_request
    def before_request():
        g.website_name = website_name

    @app.errorhandler(404)
    def page_not_found(e):
        title = '訪問頁面失敗'
        return render_template('./404.html', **locals())

    return app
