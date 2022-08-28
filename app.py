from flask import Flask, render_template, request, url_for, session, redirect
from models import db, Users, Products
from flask_migrate import Migrate
from config.env import env
from sqlalchemy import or_


app = Flask(__name__)
app.secret_key = env["KEY"]
app.config['SQLALCHEMY_DATABASE_URI'] = env["URI"]

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
                session['cargo'] = user.roles
                return redirect(url_for("ListProducts"))
        else:
            return redirect(url_for("Login"))
    return redirect(url_for("Login"))


@app.route('/logout')
def Logout():
    session.pop('id', None)
    return redirect(url_for("Login"))


""" CRUD do produto"""


@app.route('/list_products')
def ListProducts():
    if 'id' in session:

        if "search" in request.args:
            search = f"%{request.args.get('search')}%".upper()

            product = Products.query.filter(or_(Products.description.like(
                search), Products.title.like(search), Products.category.like(search)))
            return render_template("list_products.html", product=product)

        elif "filter" in request.args:

            size_filter = ['M', 'G', 'P']
            filter = str(request.args.get('filter')).upper()
            category_filter = ['MASCULINO', 'FEMININO', 'INFANTIL']

            if filter in category_filter:
                product = Products.query.filter_by(category=filter).all()

            elif filter in size_filter:
                product = Products.query.filter_by(size=filter).all()

            return render_template("list_products.html", product=product)
        else:
            product = Products.query.order_by(Products.id).all()
            return render_template("list_products.html", product=product)

    return redirect(url_for("Login"))


@app.route("/sell_products", methods=["GET", "POST"])
def SellProdutos():
    if request.method == "POST":
        for id in request.form.getlist('sell_products'):
            produtos = Products.query.get(id)
            if int(produtos.quantity) != 0:
                produtos.quantity -= 1
                db.session.commit()
        return redirect(url_for("ListProducts"))
    return redirect(url_for("Login"))


@app.route('/delete_products', methods=["GET", "DELETE"])
def DeleteProducts():
    if 'id' in session and session['cargo'] != "vendedor":
        return render_template("delete_products.html")
    return redirect(url_for("Login"))


@app.route('/insert_products', methods=["GET", "POST"])
def InsertProducts():
    if 'id' in session and session['cargo'] != "vendedor":
        return render_template("insert_products.html")
    return redirect(url_for("Login"))


""" CRUD do vendedor """


@app.route('/insert_seller', methods=["GET", "POST"])
def InsertSeller():
    if 'id' in session and session['cargo'] != "vendedor":
        return render_template("insert_seller.html")
    return redirect(url_for("Login"))


""" @app.route('/delete_seller')
def DeleteSeller():
     pass

@app.route('/list_seller')    
def ListSeller():
     pass

@app.route('/update_seller')
def UpdateSeller():
     pass """


if __name__ == '__main__':
    app.run(debug=True)
