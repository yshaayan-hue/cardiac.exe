from backend.app import app
from backend.extensions import db
from backend.models import Product


with app.app_context():

    Product.query.delete()

    db.session.commit()

    print("All products deleted.")