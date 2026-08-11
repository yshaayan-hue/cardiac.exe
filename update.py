from backend.app import app, db, Product


with app.app_context():

    products = Product.query.order_by(Product.id).all()

    images = [
        "card_a.png",
        "card_b.png",
        "card_c.png",
        "card_a.png",
        "card_b.png",
        "card_c.png"
    ]

    for product, image in zip(products, images):
        product.image = image

    db.session.commit()

    print("Product images updated.")