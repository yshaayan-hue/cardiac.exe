from extensions import db


class Order(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    email = db.Column(
        db.String(255),
        nullable=False
    )

    total = db.Column(
        db.Integer,
        nullable=False
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="Pending"
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.now()
    )


class OrderItem(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    order_id = db.Column(
        db.Integer,
        db.ForeignKey("order.id"),
        nullable=False
    )

    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id"),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    price = db.Column(
        db.Integer,
        nullable=False
    )