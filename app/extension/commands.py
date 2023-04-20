from app.extension.database import db
from app.models.tables import (Email, PhoneNumber, Roles, User, UserEmail,
                               UserPhoneNumber)


def create_db():
    """Criar banco de dados"""
    db.create_all()


def drop_db():
    """Apagar banco de dados"""
    db.drop_all()


def create_admin():
    """Criar administrador do sistema"""

    email = Email(
        e_mail='teste@gmail.com'
    )

    db.session.add(email)
    db.session.commit()

    phone_number_ = PhoneNumber(
        phone_number='999999999'
    )

    db.session.add(phone_number_)
    db.session.commit()

    email = Email.query.order_by(
        Email.id.desc()
    ).first()

    phone_number_ = PhoneNumber.query.order_by(
        PhoneNumber.id.desc()
    ).first()

    admin = Roles(roles='administrador')
    db.session.add(admin)
    db.session.commit()

    user = User(
        user='Admin',
        password='12345678',
        roles_fk=1,
    )

    db.session.add(user)
    db.session.commit()

    user = User.query.order_by(
        User.id.desc()
    ).first()

    user_email = UserEmail(
        user_fk=user.id,
        e_mail_fk=int(email.id),
    )

    db.session.add(user_email)
    db.session.commit()

    user_phone_number = UserPhoneNumber(
        user_fk=user.id,
        phone_number_fk=int(phone_number_.id),
    )

    db.session.add(user_phone_number)
    db.session.commit()

    db.session.add(user)
    db.session.commit()


def init_app(app):
    # add multiple commands in a bulk
    for command in [create_admin, drop_db, create_db]:
        app.cli.add_command(app.cli.command()(command))

    # add a single command
    # @app.cli.command()
    # @click.option('--username', '-u')
    # @click.option('--password', '-p')
    # def add_user(username, password):
    #     """Adds a new user to the database"""
    #     return create_user(username, password)

# pip freeze --local | grep -v '^\-e' | cut -d = -f 1  |
# xargs -n1 pip install -U
