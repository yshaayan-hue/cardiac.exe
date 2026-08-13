from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request
)

from extensions import db
from models import Product


cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/cart/add/<int:product_id>")
def add_to_cart(product_id):

    product = Product.query.get_or_404(product_id)

    cart = session.get("cart", {})

    product_id_string = str(product.id)

    if product_id_string in cart:

        if cart[product_id_string] < product.stock:
            cart[product_id_string] += 1

    else:

        cart[product_id_string] = 1

    session["cart"] = cart
    session.modified = True

    return redirect(url_for("cart.cart"))


@cart_bp.route("/cart")
def cart():

    cart = session.get("cart", {})

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():

        product = db.session.get(
            Product,
            int(product_id)
        )

        if product:

            subtotal = product.price * quantity

            cart_items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal
            })

            total += subtotal

    return render_template(
        "cart.html",
        cart_items=cart_items,
        total=total
    )


@cart_bp.route(
    "/cart/update/<int:product_id>",
    methods=["POST"]
)
def update_cart(product_id):

    cart = session.get("cart", {})

    product_id = str(product_id)

    if product_id not in cart:
        return redirect(url_for("cart.cart"))

    action = request.form.get("action")

    if action == "increase":

        product = db.session.get(
            Product,
            int(product_id)
        )

        if product and cart[product_id] < product.stock:
            cart[product_id] += 1

    elif action == "decrease":

        cart[product_id] -= 1

        if cart[product_id] <= 0:
            del cart[product_id]

    session["cart"] = cart
    session.modified = True

    return redirect(url_for("cart.cart"))


@cart_bp.route(
    "/cart/remove/<int:product_id>",
    methods=["POST"]
)
def remove_from_cart(product_id):

    cart = session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    session["cart"] = cart
    session.modified = True

    return redirect(url_for("cart.cart"))