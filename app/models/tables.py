from flask_login import UserMixin
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

from app.extension.database import db


class User(db.Model, UserMixin):  # type: ignore

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    roles_fk = db.Column(db.Integer, db.ForeignKey('roles.id'))
    users_roles = db.relationship('Roles', backref='User')

    @property
    def password(self):
        raise AttributeError("A senha não é um atributo legível!!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_user(cls, user: str):
        query = cls.query.filter_by(
            user=user,
        ).join(
            Roles,
            cls.roles_fk == Roles.id
        ).first()

        return query


class Roles(db.Model):  # type: ignore

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    roles = db.Column(db.String(), nullable=False)

    def __init__(self, roles):
        self.roles = roles


class UserEmail(db.Model):  # type: ignore

    __tablename__ = "user_email"

    id = db.Column(db.Integer, primary_key=True)
    user_fk = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref="user_email")
    e_mail_fk = db.Column(
        db.Integer, db.ForeignKey('email.id'), nullable=False)
    user_emails = db.relationship('Email', backref='user_email')


class Email(db.Model):  # type: ignore

    __tablename__ = "email"

    id = db.Column(db.Integer, primary_key=True)
    e_mail = db.Column(db.String(), nullable=False)


class UserPhoneNumber(db.Model):  # type: ignore

    __tablename__ = "user_phone_number"

    id = db.Column(db.Integer, primary_key=True)
    user_fk = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref="user_phone_number")
    phone_number_fk = db.Column(db.Integer, db.ForeignKey(
        'phone_number.id'), nullable=False)
    phone_numbers = db.relationship(
        'PhoneNumber', backref="user_phone_number")


class PhoneNumber(db.Model):  # type: ignore

    __tablename__ = "phone_number"

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(), nullable=False)


class Product(db.Model):  # type: ignore

    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)

    size_fk = db.Column(db.Integer, db.ForeignKey('size.id'), nullable=False)
    product_sizes = db.relationship("Size", backref="product")

    quantity = db.Column(db.Integer, nullable=False)

    category_fk = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)
    product_categoreis = db.relationship("Category", backref="product")

    purchase_price = db.Column(db.Float, nullable=False)
    sale_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(), nullable=False)
    removal = db.Column(db.String(), nullable=True)

    @classmethod
    def get_product(cls, id: int):

        query = db.session.query(
            cls.title,
            cls.sale_price,
            cls.quantity,
            cls.description,
            cls.purchase_price,
            Category.category,
            Size.size
        ).filter(
            cls.id == id,
        ).join(
            Category,
            cls.category_fk == Category.id
        ).join(
            Size,
            cls.size_fk == Size.id
        ).first()

        return query

    @classmethod
    def get_products(cls):

        query = db.session.query(
            cls.title,
            cls.sale_price,
            cls.quantity,
            cls.description,
            cls.id,
            cls.purchase_price,
            Category.category,
            Size.size
        ).join(
            Category,
            cls.category_fk == Category.id
        ).join(
            Size,
            cls.size_fk == Size.id
        ).all()

        return query

    @classmethod
    def search(cls, search: str):

        query = db.session.query(
            cls.title,
            cls.sale_price,
            cls.quantity,
            cls.description,
            cls.id,
            cls.purchase_price,
            Category.category,
            Size.size
        ).filter(
            or_(
                cls.description.like(
                    f"%{search}%".upper()
                ),
                cls.title.like(
                    f"%{search}%".upper()
                ),
                Category.category.like(
                    f"%{search}%".upper()
                )
            )
        ).join(
            Category,
            cls.category_fk == Category.id
        ).join(
            Size,
            cls.size_fk == Size.id
        ).all()

        return query

    @classmethod
    def update_product(cls, id: int, **kwargs):

        query = cls.query.get(id)

        match kwargs:
            case {'quantity': value}:

                if int(query.quantity) != 0:
                    query.quantity -= value

            case {'title': value}:
                query.title = value

            case {'purchase_price': value}:
                query.purchase_price = value

            case {'sale_price': value}:
                query.sale_price = value

            case {'description': value}:
                query.description = value

            case {'removal': value}:

                query.removal = value
        db.session.commit()

    @classmethod
    def delete_product(cls, id: int):

        query = cls.query.get(id)

        db.session.delete(query)
        db.session.commit()

    @classmethod
    def insert_product(cls, **kwargs):
        query = cls(**kwargs)
        db.session.add(query)
        db.session.commit()


class Category(db.Model):  # type: ignore

    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String())


class Size(db.Model):  # type: ignore

    __tablename__ = "size"

    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String())
