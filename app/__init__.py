import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .database import get_db, close_db
from .commands import init_app_commands

csrf = CSRFProtect()

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    csrf.init_app(app)

    app.config.from_mapping(
        SECRET_KEY = "dev",
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path, exist_ok=True)
        logs_location = os.path.dirname(app.config["LOG_FILE_PATH"])
        os.makedirs(logs_location, exist_ok=True)
        f = open(app.config["LOG_FILE_PATH"], "x")
        f.close()

    except OSError:
        pass

    init_app_commands(app)

    from .controllers.index_controller import index_blueprint
    from .controllers.sweepstakes_controller import sweepstakes_blueprint
    from .controllers.auth_controller import auth_blueprint
    from .controllers.admin_controller import admin_blueprint


    @app.before_request
    def before_each_request():
        get_db()

    @app.after_request
    def after_each_request(response):
        close_db()
        return response

    app.register_blueprint(index_blueprint)
    app.register_blueprint(sweepstakes_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(admin_blueprint)
    
    app.add_url_rule("/", endpoint="index")

    return app