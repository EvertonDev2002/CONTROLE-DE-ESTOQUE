from flask import Flask, render_template, request, url_for, session, redirect
from models import db, User, Product
from flask_migrate import Migrate
from config.env import env
from sqlalchemy import or_

app = Flask(__name__)
app.secret_key = env["KEY"]
app.config['SQLALCHEMY_DATABASE_URI'] = env["HEROKU"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
        user = User.query.filter_by(cpf=request.form['cpf']).first()
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

            product = Product.query.filter(or_(Product.description.like(
                search), Product.title.like(search), Product.category.like(search)))
            return render_template("list_products.html", product=product)

        elif "filter" in request.args:

            filter = str(request.args.get('filter')).upper()

            if filter in ['MASCULINO', 'FEMININO', 'INFANTIL']:
                product = Product.query.filter_by(category=filter).all()

            elif filter in ['M', 'G', 'P']:
                product = Product.query.filter_by(size=filter).all()

            return render_template("list_products.html", product=product)
        else:
            product = Product.query.order_by(Product.id).all()
            return render_template("list_products.html", product=product)

    return redirect(url_for("Login"))


@app.route("/sell_products", methods=["GET", "POST"])
def SellProdutos():
    if request.method == "POST":
        for id in request.form.getlist('sell_products'):
            produtos = Product.query.get(id)
            if int(produtos.quantity) != 0:
                produtos.quantity -= 1
                db.session.commit()
        return redirect(url_for("ListProducts"))
    return redirect(url_for("Login"))


@app.route('/delete_products', methods=["GET", "POST"])
def DeleteProducts():
    if 'id' in session and session['cargo'] in ['gerente', 'administrador']:
        return render_template("delete_products.html")
    return redirect(url_for("Login"))


@app.route('/insert_products', methods=["GET", "POST"])
def InsertProducts():
    if 'id' in session and session['cargo'] in ['gerente', 'administrador']:
        if request.method == "POST":
            product = Product(title=request.form['title'], size=request.form['size'], quantity=request.form['quantity'], category=request.form['category'],
                              sale_price=request.form['price'], description=request.form['description'], purchase_price=request.form['purchase_price'])
            db.session.add(product)
            db.session.commit()
        else:
            return render_template("insert_products.html")
    return redirect(url_for("Login"))


""" CRUD do vendedor """


@app.route('/insert_seller', methods=["GET", "POST"])
def InsertSeller():
    if 'id' in session and session['cargo'] in ['gerente', 'administrador']:
        if request.method == "POST":
            vendedor = User(cpf=request.form['cpf'], password=request.form['password'], roles='vendedor',
                            name=request.form['name'], e_mail=request.form['e_mail'], phone_number=request.form['phone_number'])
            db.session.add(vendedor)
            db.session.commit()
        return render_template("insert_seller.html")
    return redirect(url_for("Login"))


if __name__ == '__main__':
    db.create_all()
    app.run()
