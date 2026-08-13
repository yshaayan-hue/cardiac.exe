from flask import Blueprint, render_template

from models import Product


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():

    products = Product.query.all()

    return render_template(
        "home.html",
        products=products
    )


@main_bp.route("/products")
def products():

    products = Product.query.all()

    return render_template(
        "home.html",
        products=products
    )


@main_bp.route("/products/<int:product_id>")
def product_detail(product_id):

    product = Product.query.get_or_404(product_id)

    return render_template(
        "product_detail.html",
        product=product
    )