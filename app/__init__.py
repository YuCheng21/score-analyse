from flask import Flask, render_template
import os

from .config.flask import config as flask_config
from .config.base import project_path

from .view.root import app as root


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(flask_config[config_name])
    app.static_folder = os.path.join(project_path, 'app', 'static')
    app.template_folder = os.path.join(project_path, 'app', 'templates')

    app.register_blueprint(root)

    @app.errorhandler(404)
    def page_not_found(e):
        title = '訪問頁面失敗'
        return render_template('./404.html', **locals())

    return app
