from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request
)

try:
    from ..extensions import db
    from ..models import Product, Order, OrderItem
except ImportError:
    from extensions import db
    from models import Product, Order, OrderItem


orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/order", methods=["GET", "POST"])
def order():

    cart = session.get("cart", {})

    cart_items = []
    total = 0

    # -------------------------
    # Build cart
    # -------------------------

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

    # -------------------------
    # Prevent empty orders
    # -------------------------

    if not cart_items:
        return redirect(
            url_for("cart.cart")
        )

    # -------------------------
    # Handle order submission
    # -------------------------

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip()

        # Basic email validation
        if not email or "@" not in email:

            return render_template(
                "order.html",
                cart_items=cart_items,
                total=total,
                error="Please enter a valid email address."
            )

        # -------------------------
        # Create Order
        # -------------------------

        new_order = Order(
            email=email,
            total=total,
            status="Pending"
        )

        db.session.add(new_order)

        # Flush so new_order.id is available
        db.session.flush()

        # -------------------------
        # Create Order Items
        # -------------------------

        for item in cart_items:

            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item["product"].id,
                quantity=item["quantity"],
                price=item["product"].price
            )

            db.session.add(order_item)

        # -------------------------
        # Save order
        # -------------------------

        db.session.commit()

        # -------------------------
        # Clear cart
        # -------------------------

        session.pop("cart", None)

        # -------------------------
        # Success page
        # -------------------------

        return render_template(
            "order_success.html",
            order=new_order
        )

    # -------------------------
    # GET request
    # -------------------------

    return render_template(
        "order.html",
        cart_items=cart_items,
        total=total
    )