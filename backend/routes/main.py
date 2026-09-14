from flask import Blueprint, render_template

try:
    from ..extensions import db
    from ..models import Product
except ImportError:
    from extensions import db
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
    related_products = Product.query.filter(Product.id != product_id).limit(3).all()

    return render_template(
        "product_detail.html",
        product=product,
        related_products=related_products
    )


@main_bp.route("/login")
def login():
    return render_template("auth/login.html")


@main_bp.route("/register")
def register():
    return render_template("auth/register.html")