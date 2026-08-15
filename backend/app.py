from flask import Flask

try:
    from .config import Config
    from .extensions import db
    from .routes import main_bp, cart_bp, orders_bp
except ImportError:
    from config import Config
    from extensions import db
    from routes import main_bp, cart_bp, orders_bp


app = Flask(
    __name__,
    template_folder="../frontend/templates",
    static_folder="../frontend/static"
)

app.config.from_object(Config)

db.init_app(app)


app.register_blueprint(main_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(orders_bp)


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)