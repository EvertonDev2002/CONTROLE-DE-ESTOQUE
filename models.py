from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    roles = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    e_mail = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String(), nullable=False)

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(), nullable=False)
    size = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    price = db.Column(db.Float, nullable=False)
