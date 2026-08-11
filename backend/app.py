from flask import Flask, render_template, session, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy



app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

app.secret_key = "dev-secret-key-change-later"

# -------------------------
# Database configuration
# -------------------------

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cardiac.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# -------------------------
# Product Model
# -------------------------

class Product(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    price = db.Column(
        db.Integer,
        nullable=False
    )

    stock = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )

    image = db.Column(
        db.String(200)
    )


# -------------------------
# Create database
# -------------------------

with app.app_context():
    db.create_all()


# -------------------------
# Routes
# -------------------------

@app.route("/")
def home():

    products = Product.query.all()

    return render_template(
        "home.html",
        products=products
    )


@app.route("/products")
def products():

    products = Product.query.all()

    return render_template(
        "home.html",
        products=products
    )


@app.route("/products/<int:product_id>")
def product_detail(product_id):

    product = Product.query.get_or_404(product_id)

    return render_template(
        "product_detail.html",
        product=product
    )

@app.route("/cart/add/<int:product_id>")
def add_to_cart(product_id):

    product = Product.query.get_or_404(product_id)

    cart = session.get("cart", {})

    product_id_string = str(product.id)

    if product_id_string in cart:

        cart[product_id_string] += 1

    else:

        cart[product_id_string] = 1

    session["cart"] = cart

    return redirect(url_for("cart"))


@app.route("/cart")
def cart():

    cart = session.get("cart", {})

    cart_items = []

    total = 0

    for product_id, quantity in cart.items():

        product = Product.query.get(int(product_id))

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


# ADD THIS BELOW THE CART ROUTE
@app.route("/cart/update/<int:product_id>", methods=["POST"])
def update_cart(product_id):

    cart = session.get("cart", {})

    product_id = str(product_id)

    # Check whether the product exists in the cart
    if product_id not in cart:
        return redirect(url_for("cart"))

    # Get the requested action from the form
    action = request.form.get("action")

    # Increase quantity
    if action == "increase":

        product = Product.query.get(product_id)

        if product and cart[product_id] < product.stock:
            cart[product_id] += 1

    # Decrease quantity
    elif action == "decrease":

        cart[product_id] -= 1

        # Remove product if quantity reaches zero
        if cart[product_id] <= 0:
            del cart[product_id]

    session["cart"] = cart
    session.modified = True

    return redirect(url_for("cart"))


    




# ADD THIS BELOW update_cart

@app.route("/cart/remove/<int:product_id>", methods=["POST"])
def remove_from_cart(product_id):

    cart = session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    session["cart"] = cart
    session.modified = True

    return redirect(url_for("cart"))

# -------------------------
# Run application
# -------------------------

if __name__ == "__main__":
    app.run(debug=True)