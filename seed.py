from backend.app import app
from backend.extensions import db
from backend.models import Product


with app.app_context():

    products = [
        Product(
            name="Card A",
            description="Custom collectible card.",
            price=499,
            stock=10,
            image="card_a.png"
        ),

        Product(
            name="Card B",
            description="Custom collectible card.",
            price=699,
            stock=10,
            image="card_b.png"
        ),

        Product(
            name="Card C",
            description="Custom collectible card.",
            price=899,
            stock=10,
            image="card_c.png"
        )
    ]

    for product in products:
        db.session.add(product)

    db.session.commit()

    print("Products added successfully.")