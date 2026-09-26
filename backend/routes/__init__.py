from .main import main_bp
from .cart import cart_bp
from .orders import orders_bp
from .auth import auth_bp
from .admin import admin_bp

__all__ = [
    "main_bp",
    "cart_bp",
    "orders_bp",
    "auth_bp",
]