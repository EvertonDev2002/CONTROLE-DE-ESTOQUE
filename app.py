from flask import Flask, render_template, request, url_for
#from flask_migrate import Migrate
#from models import db, Users, Products

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://<user>:<password>@<endress>:5432/<database>"

#db.init_app(app)

#migrate = Migrate(app, db)

@app.route('/login')
def Login():
     pass

""" CRUD do produto"""

@app.route('/')
def ListProducts():
     return render_template("index.html")

@app.route('/delete_products')
def DeleteProducts():
     pass

@app.route('/insert_products')
def InsertProducts():
     pass

@app.route('/update_products')
def UpdateProducts():
     pass


""" CRUD do vendedor """

@app.route('/insert_Seller')
def InsertSeller():
     pass

@app.route('/delete_seller')
def DeleteSeller():
     pass

@app.route('/list_seller')
def ListSeller():
     pass

@app.route('/update_seller')
def UpdateSeller():
     pass


if __name__ == '__main__':
     app.run()