from flask import Flask, render_template, \
     request, url_for, session, redirect, abort
from flask_migrate import Migrate
from models import db, Users, Products
from config.env import env

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = env["URI"]
app.secret_key = env["KEY"]

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def Login():
     if 'id' in session:
          return redirect(url_for("ListProducts"))

     return render_template("index.html")

@app.route("/check_login", methods=["POST"])
def CheckLogin():
     if request.method == 'POST':
          user = Users.query.filter_by(cpf=request.form['cpf']).first()
          if user:
               if user.password == request.form['password']:
                    session['id'] = user.id
                    return redirect(url_for("ListProducts"))
          else:
              return redirect(url_for("Login"))
     return redirect(url_for("Login"))

@app.route('/logout')
def Logout():
     session.pop('id', None)
     return  redirect(url_for("Login"))

""" CRUD do produto"""

@app.route('/list_products')
def ListProducts():
     if 'id' in session:
           return render_template("list_products.html")
     return redirect(url_for("Login"))


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
     app.run(debug=True)