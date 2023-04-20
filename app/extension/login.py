from flask_login import LoginManager

from app.models.tables import User

login_manager = LoginManager()


def init_app(app):
    login_manager.init_app(app)
    login_manager.login_view = 'blueprints.login'  # type: ignore

    @login_manager.user_loader
    def get_user(id):
        return User.query.filter_by(id=id).first()
