from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    request,
    jsonify
)

try:
    from ..extensions import db
    from ..models import Product
except ImportError:
    from extensions import db
    from models import Product

cart_bp = Blueprint("cart", __name__)


@cart_bp.route("/cart/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):

    product = Product.query.get_or_404(product_id)
    cart = session.get("cart", {})
    product_id_string = str(product.id)

    qty_to_add = request.form.get("quantity", type=int) or 1
    if qty_to_add < 1:
        qty_to_add = 1

    current_qty = cart.get(product_id_string, 0)
    new_qty = min(current_qty + qty_to_add, product.stock)
    cart[product_id_string] = new_qty

    session["cart"] = cart
    session.modified = True

    if request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json:
        return jsonify({
            "success": True,
            "message": f"{product.name} added to cart",
            "cart_count": sum(cart.values())
        })

    return redirect(request.referrer or url_for("cart.cart"))


@cart_bp.route("/cart")
def cart():

    cart = session.get("cart", {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():

        product = db.session.get(Product, int(product_id))

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
    product_id_string = str(product_id)

    if product_id_string not in cart:
        if request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json:
            return jsonify({"error": "Item not in cart"}), 404
        return redirect(url_for("cart.cart"))

    product = db.session.get(Product, product_id)
    action = request.form.get("action")
    raw_qty = request.form.get("quantity")

    if action == "increase":
        if product and cart[product_id_string] < product.stock:
            cart[product_id_string] += 1
    elif action == "decrease":
        cart[product_id_string] -= 1
        if cart[product_id_string] <= 0:
            del cart[product_id_string]
    elif raw_qty is not None:
        try:
            qty = int(raw_qty)
            if qty <= 0:
                del cart[product_id_string]
            else:
                max_stock = product.stock if product else qty
                cart[product_id_string] = min(qty, max_stock)
        except ValueError:
            pass

    session["cart"] = cart
    session.modified = True

    if request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json:
        curr_qty = cart.get(product_id_string, 0)
        item_subtotal = (product.price * curr_qty) if product else 0
        total = sum(
            (db.session.get(Product, int(pid)).price * q)
            for pid, q in cart.items()
            if db.session.get(Product, int(pid))
        )
        return jsonify({
            "success": True,
            "cart_count": sum(cart.values()),
            "item_qty": curr_qty,
            "subtotal": item_subtotal,
            "total": total
        })

    return redirect(url_for("cart.cart"))


@cart_bp.route(
    "/cart/remove/<int:product_id>",
    methods=["POST"]
)
def remove_from_cart(product_id):

    cart = session.get("cart", {})
    product_id_string = str(product_id)

    if product_id_string in cart:
        del cart[product_id_string]

    session["cart"] = cart
    session.modified = True

    if request.headers.get("X-Requested-With") == "XMLHttpRequest" or request.is_json:
        total = sum(
            (db.session.get(Product, int(pid)).price * q)
            for pid, q in cart.items()
            if db.session.get(Product, int(pid))
        )
        return jsonify({
            "success": True,
            "cart_count": sum(cart.values()),
            "total": total
        })

    return redirect(url_for("cart.cart"))