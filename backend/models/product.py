try:
    from ..extensions import db
except ImportError:
    from extensions import db


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