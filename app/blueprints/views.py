from flask import redirect, render_template, request, session, url_for
from flask_login import login_required, login_user, logout_user

from app.extension.database import db
from app.models.forms import LoginForm
from app.models.tables import (Category, Email, PhoneNumber, Product, Size,
                               User, UserEmail, UserPhoneNumber)


def login():

    form = LoginForm()
    user = User()

    if request.method == 'POST':
        if form.validate_on_submit():

            query = user.get_user(request.form['user'])

            if query.user and query.verify_password(request.form['password']):

                session['id'] = query.id
                session['user'] = query.user
                session['cargo'] = query.roles_fk

                login_user(query)

                return redirect(url_for("blueprints.list_products"))
    return render_template("index.html", form=form)


@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("blueprints.login"))

# CRUD do produto


@login_required
def list_products():

    product = Product()

    query = product.get_products()

    if "search" in request.args:

        query = product.search(str(request.args.get('search')))

    return render_template("list_products.html", product=query)


@ login_required
def sell_product():
    if request.method == "POST":

        product = Product()

        for id in request.form.getlist('sell_products'):

            product.update_product(int(id), quantity=1)

        return redirect(url_for("blueprints.list_products"))
    return redirect(url_for("log_in"))


@ login_required
def delete_product(id: int):

    query = Product()
    query.delete_product(id)

    return redirect(url_for("blueprints.list_products"))


@ login_required
def delete_products_list():
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


@login_required
def insert_products():
    if request.method == "POST":

        query = Product()

        products = {
            "title": str(request.form['title']).upper(),
            "size_fk": int(request.form['size']),
            "quantity": int(request.form['quantity']),
            "category_fk": int(request.form['category']),
            "sale_price": float(request.form['price']),
            "description": str(request.form['description']).upper(),
            "purchase_price": float(request.form['purchase_price']),
        }

        query.insert_product(**products)

    category = Category.query.order_by(Category.category).all()
    size = Size.query.order_by(Size.size).all()

    return render_template(
        "insert_products.html",
        category=category,
        size=size
    )


@login_required
def update_products(id: int):
    product = Product()
    match request.method:
        case "POST":

            return redirect(url_for("blueprints.list_products"))
        case "GET":
            query = product.get_product(id)

            return render_template('update_products.html', product=query)

# CRUD do vendedor


@login_required
def insert_seller():
    if 'id' in session and session['cargo'] in ['gerente', 'administrador']:
        if request.method == "POST":

            email = Email(
                e_mail=request.form['e_mail']
            )

            db.session.add(email)
            db.session.commit()

            phone_number_ = PhoneNumber(
                phone_number=request.form['phone_number']
            )

            db.session.add(phone_number_, email)
            db.session.commit()

            email = Email.query.order_by(
                Email.id.desc()
            ).first()
            phone_number_ = PhoneNumber.query.order_by(
                PhoneNumber.id.desc()
            ).first()

            seller = User(
                user=str(request.form['user']),
                password=request.form['password'],
                roles_fk=int(3),
            )

            db.session.add(seller)
            db.session.commit()

            seller = User.query.order_by(
                User.id.desc()
            ).first()

            user_email = UserEmail(
                user_fk=seller.id,
                e_mail_fk=int(email.id),
            )

            db.session.add(user_email)
            db.session.commit()

            user_phone_number = UserPhoneNumber(
                user_fk=seller.id,
                phone_number_fk=int(phone_number_.id),
            )

            db.session.add(user_phone_number)
            db.session.commit()

            return render_template("insert_seller.html")
    return redirect(url_for("log_in"))
