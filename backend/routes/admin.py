from flask import Blueprint, jsonify

from ..decorators import admin_required


admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/api/admin"
)


@admin_bp.route("/test", methods=["GET"])
@admin_required
def admin_test():
    return jsonify({
        "message": "Admin access granted"
    }), 200