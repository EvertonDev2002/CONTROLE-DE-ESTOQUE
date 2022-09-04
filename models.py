from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    roles = db.Column(db.String(13), nullable=False)
    name = db.Column(db.String(), nullable=False)
    e_mail = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String(18), nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    size = db.Column(db.String(1), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(9), nullable=False)
    purchase_price = db.Column(db.Float, nullable=False)
    sale_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(), nullable=False)
