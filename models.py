from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    roles_fk = db.Column(db.Integer, db.ForeignKey('roles.id'))
    users_roles = db.relationship('Roles', backref='User')


class Roles(db.Model):

    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    roles = db.Column(db.String(), nullable=False)


class User_Email(db.Model):

    __tablename__ = "user_email"

    id = db.Column(db.Integer, primary_key=True)
    user_fk = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref="user_email")
    e_mail_fk = db.Column(
        db.Integer, db.ForeignKey('email.id'), nullable=False)
    user_emails = db.relationship('Email', backref='user_email')


class Email(db.Model):

    __tablename__ = "email"

    id = db.Column(db.Integer, primary_key=True)
    e_mail = db.Column(db.String(), nullable=False)


class User_Phone_Number(db.Model):

    __tablename__ = "user_phone_number"

    id = db.Column(db.Integer, primary_key=True)
    user_fk = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref="user_phone_number")
    phone_number_fk = db.Column(db.Integer, db.ForeignKey(
        'phone_number.id'), nullable=False)
    phone_numbers = db.relationship(
        'Phone_Number', backref="user_phone_number")


class Phone_Number(db.Model):

    __tablename__ = "phone_number"

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(), nullable=False)


class Product(db.Model):

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


class Category(db.Model):

    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String())


class Size(db.Model):

    __tablename__ = "size"

    id = db.Column(db.Integer, primary_key=True)
    size = db.Column(db.String())
