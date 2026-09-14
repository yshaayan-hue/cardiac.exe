from itsdangerous import URLSafeTimedSerializer
from itsdangerous.exc import BadSignature, SignatureExpired

from ..config import Config


TOKEN_MAX_AGE = 30 * 60


def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(
        Config.SECRET_KEY
    )

    return serializer.dumps(
        email,
        salt="email-verification"
    )


def verify_verification_token(token):
    serializer = URLSafeTimedSerializer(
        Config.SECRET_KEY
    )

    try:
        return serializer.loads(
            token,
            salt="email-verification",
            max_age=TOKEN_MAX_AGE
        )
    except (BadSignature, SignatureExpired):
        return None