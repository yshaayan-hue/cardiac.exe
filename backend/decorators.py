from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from .extensions import db
from .models import User


def admin_required(fn=None):
    """
    Decorator to protect admin routes.
    Ensures a valid JWT is present, the corresponding user exists in the database,
    and the user has the 'admin' role.
    Supports both @admin_required and @admin_required() syntax.
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()

            user_id = get_jwt_identity()

            try:
                user = db.session.get(User, int(user_id))
            except (ValueError, TypeError):
                user = None

            if not user:
                return jsonify({
                    "error": "User not found"
                }), 404

            if user.role != "admin":
                return jsonify({
                    "error": "Admin access required"
                }), 403

            return f(*args, **kwargs)

        return wrapper

    if callable(fn):
        return decorator(fn)
    return decorator
