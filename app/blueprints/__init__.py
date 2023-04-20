from flask import Blueprint

from .views import (delete_product, insert_products, insert_seller,
                    list_products, login, logout, sell_product,
                    update_products)

bp = Blueprint(
    "blueprints",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path='/app/blueprints/static/'
)

bp.add_url_rule(
    rule="/",
    view_func=login,
    endpoint='login',
    methods=['POST', 'GET'],
)
bp.add_url_rule(
    rule="/logout",
    view_func=logout,
    endpoint='logout',
    methods=['GET'],
)
bp.add_url_rule(
    rule="/list_products",
    view_func=list_products,
    endpoint='list_products',
    methods=["GET"]
)
bp.add_url_rule(
    rule="/sell_products",
    view_func=sell_product,
    methods=["GET", "POST"],
)
bp.add_url_rule(
    rule="/delete_products/<id>",
    endpoint='delete_product',
    view_func=delete_product,  # type: ignore
    methods=["GET"],
)
bp.add_url_rule(
    rule="/insert_products",
    view_func=insert_products,
    methods=["GET", "POST"],
)
bp.add_url_rule(
    rule="/update_products/<id>",
    view_func=update_products,  # type: ignore
    methods=["GET", "POST"],
)
bp.add_url_rule(
    rule="/insert_seller",
    view_func=insert_seller,
    methods=["GET", "POST"],
)


def init_app(app):
    app.register_blueprint(bp)
