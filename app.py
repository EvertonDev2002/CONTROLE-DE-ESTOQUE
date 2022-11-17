from flask import Flask, render_template, request, url_for, session, redirect
from models import db, User, Product, Roles, Category, Size, Email, Phone_Number, User_Email, User_Phone_Number
from flask_migrate import Migrate
from config.env import env
from sqlalchemy import or_
from bcrypt import hashpw, checkpw, gensalt

app = Flask(__name__)
app.secret_key = env["KEY"]
app.config['SQLALCHEMY_DATABASE_URI'] = env["URI"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def Login():
    if 'id' in session:
        return redirect(url_for("ListProducts"))

    return render_template("index.html")


@app.route("/check_login", methods=["GET", "POST"])
def CheckLogin():
    if request.method == 'POST':

        user = db.session.query(
            User.user,
            User.id,
            User.password,
            Roles.roles,
        ).filter(
            User.user == request.form['user']
        ).join(Roles, User.roles_fk == Roles.id).first()

        if user:
            if checkpw(request.form['password'].encode("UTF-8"), user.password.encode("UTF-8")):

                session['id'] = user.id
                session['user'] = user.user
                session['cargo'] = user.roles

                return redirect(url_for("ListProducts"))
            else:
                return redirect(url_for("Login"))
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

            product = db.session.query(
                Product.title,
                Product.sale_price,
                Product.quantity,
                Product.description,
                Product.id,
                Product.purchase_price,
                Category.category,
                Size.size
            ).filter(
                or_(
                    Product.description.like(search),
                    Product.title.like(search),
                    Category.category.like(search)
                )
            ).join(Category, Product.category_fk == Category.id).join(Size, Product.size_fk == Size.id).all()

            return render_template("list_products.html", product=product)
        else:

            product = db.session.query(
                Product.title,
                Product.sale_price,
                Product.quantity,
                Product.description,
                Product.id,
                Product.purchase_price,
                Category.category,
                Size.size
            ).join(Category, Product.category_fk == Category.id).join(Size, Product.size_fk == Size.id).all()

            return render_template("list_products.html", product=product)

    return redirect(url_for("Login"))


@app.route("/sell_products", methods=["GET", "POST"])
def SellProduct():
    if request.method == "POST":
        for id in request.form.getlist('sell_products'):

            product = Product.query.get(id)

            if int(product.quantity) != 0:
                product.quantity -= 1
                db.session.commit()

        return redirect(url_for("ListProducts"))
    return redirect(url_for("Login"))


@app.route('/delete_products', methods=["GET", "POST"])
def DeleteProducts():
    if 'id' in session and session['cargo'] in ['gerente', 'administrador']:
        if request.method == "POST":
            for i in range((len(request.form)//2)+1):
                form = {
                    'id': f'id{i}',
                    'quantity': f'quantity{i}',
                    'removal': f'removal{i}'
                }
                for id in request.form.getlist(form['id']):
                    for quantity in request.form.getlist(form['quantity']):
                        for removal in request.form.getlist(form['removal']):
                            product = Product.query.get(id)
                            if int(product.quantity) != 0:
                                product.quantity -= int(quantity)
                                product.removal = str(removal)
                                db.session.commit()
            return redirect(url_for("ListProducts"))
        return render_template("delete_products.html")
    return redirect(url_for("Login"))


@app.route('/insert_products', methods=["GET", "POST"])
def InsertProducts():
    if 'id' in session and session['cargo'] in ['gerente', 'administrador']:
        if request.method == "POST":

            dict_product = {
                'title': str(request.form['title']).upper(),
                'size_fk': int(request.form['size']),
                'quantity': int(request.form['quantity']),
                'category_fk': int(request.form['category']),
                'sale_price': float(request.form['price']),
                'description': str(request.form['description']).upper(),
                'purchase_price': float(request.form['purchase_price']),
            }

            product = Product(
                title=dict_product['title'],
                size_fk=dict_product['size_fk'],
                quantity=dict_product['quantity'],
                category_fk=dict_product['category_fk'],
                sale_price=dict_product['sale_price'],
                description=dict_product['description'],
                purchase_price=dict_product['purchase_price']
            )

            db.session.add(product)
            db.session.commit()

        else:
            if request.method == "GET":

                category = Category.query.order_by(Category.category).all()
                size = Size.query.order_by(Size.size).all()

                return render_template("insert_products.html", category=category, size=size)
    return redirect(url_for("Login"))

@app.route('/update_products', methods=["GET", "POST"])
def UpdateProducts():
    return "Em desenvolvimento"

""" CRUD do vendedor """


@app.route('/insert_seller', methods=["GET", "POST"])
def InsertSeller():
    if 'id' in session and session['cargo'] in ['gerente', 'administrador']:
        if request.method == "POST":

            email = Email(
                e_mail=request.form['e_mail']
            )
            db.session.add(email)
            db.session.commit()

            phone_number_ = Phone_Number(
                phone_number=request.form['phone_number']
            )

            db.session.add(phone_number_, email)
            db.session.commit()

            email = Email.query.order_by(Email.id.desc()).first()
            phone_number_ = Phone_Number.query.order_by(
                Phone_Number.id.desc()).first()

            dict_seller = {
                'user': str(request.form['user']),
                'password': hashpw(request.form['password'].encode("utf-8"), gensalt()),
                'roles_fk': int(3),
                'e_mail_fk': int(email.id),
                'phone_number_fk': int(phone_number_.id),
            }

            seller = User(
                user=dict_seller['user'],
                password=dict_seller['password'],
                roles_fk=dict_seller['roles_fk'],
            )

            db.session.add(seller)
            db.session.commit()

            seller = User.query.order_by(User.id.desc()).first()

            user_email = User_Email(
                user_fk=seller.id,
                e_mail_fk=dict_seller['e_mail_fk']
            )

            db.session.add(user_email)
            db.session.commit()

            user_phone_number = User_Phone_Number(
                user_fk=seller.id,
                phone_number_fk=dict_seller['phone_number_fk']
            )

            db.session.add(user_phone_number)
            db.session.commit()

        return render_template("insert_seller.html")
    return redirect(url_for("Login"))


if __name__ == '__main__':
    app.run(debug=True)
