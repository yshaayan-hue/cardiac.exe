from backend.app import app
from backend.extensions import db
from backend.models import Product, Order, OrderItem


def setup_function():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SECRET_KEY"] = "test-secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    with app.app_context():
        db.drop_all()
        db.create_all()
        product = Product(name="Test Product", description="Example", price=250, stock=10, image="")
        db.session.add(product)
        db.session.commit()


def test_order_post_creates_order_and_items():
    with app.test_client() as client:
        with client.session_transaction() as session:
            session["cart"] = {"1": 2}

        response = client.post(
            "/order",
            data={
                "email": "test@example.com",
            },
            follow_redirects=False,
        )

        assert response.status_code == 200

        with app.app_context():
            order = Order.query.first()
            assert order is not None
            assert order.email == "test@example.com"
            assert order.total == 500
            assert OrderItem.query.count() == 1
            assert OrderItem.query.first().price_at_purchase == 250
