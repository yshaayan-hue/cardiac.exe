import os

from dotenv import load_dotenv

load_dotenv()


BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

INSTANCE_DIR = os.path.join(
    BASE_DIR,
    "instance"
)

DATABASE_PATH = os.path.join(
    INSTANCE_DIR,
    "cardiac.db"
)


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY"
    )

    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY"
    )

    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + DATABASE_PATH
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session cookie security

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SAMESITE = "Lax"

    # Local development uses HTTP.
    # Change to True when deployed with HTTPS.

    SESSION_COOKIE_SECURE = False