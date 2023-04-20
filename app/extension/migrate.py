from flask_migrate import Migrate

from app.extension.database import db

migrate = Migrate()


def init_app(app):
    migrate.init_app(app, db)
