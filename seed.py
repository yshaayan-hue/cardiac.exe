from backend.app import app, db, Product


products = [
    Product(
        name="Custom Card A",
        description="A custom-designed collectible card.",
        price=499,
        stock=10,
        image="card_a.jpg"
    ),

    Product(
        name="Custom Card B",
        description="A premium custom collectible card.",
        price=699,
        stock=5,
        image="card_b.jpg"
    ),

    Product(
        name="Custom Card C",
        description="A limited custom-designed card.",
        price=899,
        stock=3,
        image="card_c.jpg"
    )
]
with app.app_context():

    if Product.query.count() == 0:

        for product in products:
            db.session.add(product)

        db.session.commit()

        print("Products added successfully.")

    else:

        print("Products already exist. Nothing added.")