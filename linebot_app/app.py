# Created at 2021.11.15
# Author: Sharpkoi
# Description: An application factory which builds app and
# registers some necessary extensions like sqlalchemy and flask_migrate.
# Copyright 2021 Sharpkoi. All Rights Reserved.

from typing import Dict

from flask import Flask

from linebot_app import routes
from linebot_app.extensions import db, migrate


def create_app(config: Dict):
    app = Flask(__name__)
    app.config.from_mapping(config)
    app.app_context().push()
    register_extensions(app)
    register_blueprints(app)

    return app


def register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app)


def register_blueprints(app: Flask):
    app.register_blueprint(routes.blueprint)
