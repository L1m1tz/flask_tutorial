import os

from flask import Flask
from flaskr.db import get_db


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # add db comands and close_db to the app
    from . import db
    db.init_app(app)

    # register main_blueprint to app
    from . import main
    app.register_blueprint(main.main_blueprint)
    from . import auth
    app.register_blueprint(auth.auth_blueprint)
    from . import post
    app.register_blueprint(post.post_blueprint)
    app.add_url_rule('/', endpoint='post')
    from . import profile
    app.register_blueprint(profile.profile_blueprint)

    return app
