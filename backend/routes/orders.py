from flask import Blueprint, render_template, session, redirect, url_for

from extensions import db
from models import Product


orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/order")
def order():

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

    if not cart_items:
        return redirect(url_for("cart.cart"))

    return render_template(
        "order.html",
        cart_items=cart_items,
        total=total
    )