from flask import Flask, session
from sqlalchemy import text

from .config import Config
from .extensions import db, csrf, jwt
from .routes import (
    main_bp,
    cart_bp,
    orders_bp,
    auth_bp,
    admin_bp,
)


def ensure_user_schema():
    inspector = db.inspect(db.engine)
    table_names = inspector.get_table_names()

    if "users" not in table_names:
        db.create_all()
        return

    columns = [column["name"] for column in inspector.get_columns("users")]

    if "email_verified" not in columns:
        with db.engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE users ADD COLUMN email_verified BOOLEAN NOT NULL DEFAULT 0")
            )


app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

app.config.from_object(Config)

db.init_app(app)
csrf.init_app(app)
jwt.init_app(app)

app.register_blueprint(main_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(auth_bp) 
app.register_blueprint(admin_bp)


@app.context_processor
def inject_cart_info():
    cart = session.get("cart", {})
    count = sum(cart.values()) if isinstance(cart, dict) else 0
    return dict(cart_count=count)



with app.app_context():
    ensure_user_schema()


if __name__ == "__main__":
    app.run(debug=False)