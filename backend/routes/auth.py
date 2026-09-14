from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from ..extensions import db, csrf
from ..models import User
from ..services.email_verification import (
    generate_verification_token,
    verify_verification_token
)


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/api/auth"
)


# API endpoints use JWT authentication rather than
# Flask's browser-session authentication.
csrf.exempt(auth_bp)


@auth_bp.route("/register", methods=["POST"])
@csrf.exempt
def register():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must be JSON"
        }), 400

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    # -------------------------
    # Validate input
    # -------------------------

    if not name or not email or not password:
        return jsonify({
            "error": "Name, email and password are required"
        }), 400

    if len(name) > 100:
        return jsonify({
            "error": "Name is too long"
        }), 400

    if "@" not in email or "." not in email:
        return jsonify({
            "error": "Invalid email address"
        }), 400

    if len(password) < 8:
        return jsonify({
            "error": "Password must be at least 8 characters"
        }), 400

    # -------------------------
    # Check duplicate email
    # -------------------------

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:
        return jsonify({
            "error": "Email is already registered"
        }), 409

    # -------------------------
    # Create user
    # -------------------------

    user = User(
        name=name,
        email=email,
        email_verified=False,
        role="customer"
    )

    user.set_password(password)

    db.session.add(user)

    try:

        db.session.commit()

    except Exception:

        db.session.rollback()

        return jsonify({
            "error": "Could not create account"
        }), 500

    # -------------------------
    # Generate verification token
    # -------------------------

    token = generate_verification_token(
        user.email
    )

    # Development-only verification URL.
    # Replace this with a real email service before deployment.
    verification_url = (
        "http://127.0.0.1:5000/api/auth/verify/"
        + token
    )

    return jsonify({
        "message": "Registration successful. Verify your email.",
        "verification_url": verification_url
    }), 201


@auth_bp.route(
    "/verify/<token>",
    methods=["GET"]
)
def verify_email(token):

    # -------------------------
    # Validate token
    # -------------------------

    email = verify_verification_token(
        token
    )

    if not email:
        return jsonify({
            "error": "Verification link is invalid or expired"
        }), 400

    # -------------------------
    # Find user
    # -------------------------

    user = User.query.filter_by(
        email=email
    ).first()

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    # -------------------------
    # Already verified
    # -------------------------

    if user.email_verified:

        return jsonify({
            "message": "Email is already verified"
        }), 200

    # -------------------------
    # Verify email
    # -------------------------

    user.email_verified = True

    try:

        db.session.commit()

    except Exception:

        db.session.rollback()

        return jsonify({
            "error": "Could not verify email"
        }), 500

    return jsonify({
        "message": "Email verified successfully"
    }), 200


@auth_bp.route("/login", methods=["POST"])
@csrf.exempt
def login():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must be JSON"
        }), 400

    email = data.get(
        "email",
        ""
    ).strip().lower()

    password = data.get(
        "password",
        ""
    )

    # -------------------------
    # Validate input
    # -------------------------

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    # -------------------------
    # Find user
    # -------------------------

    user = User.query.filter_by(
        email=email
    ).first()

    # Use the same message for
    # invalid email and password.
    if not user:
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    # -------------------------
    # Verify password
    # -------------------------

    if not user.check_password(
        password
    ):
        return jsonify({
            "error": "Invalid email or password"
        }), 401

    # -------------------------
    # Require email verification
    # -------------------------

    if not user.email_verified:

        return jsonify({
            "error": "Please verify your email before logging in"
        }), 403

    # -------------------------
    # Generate JWT
    # -------------------------

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )

    # -------------------------
    # Return response
    # -------------------------

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 200