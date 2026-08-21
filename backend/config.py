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

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + DATABASE_PATH
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    
    SESSION_COOKIE_SECURE = False