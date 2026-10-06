from datetime import UTC, datetime, timedelta

from jose import jwt
import bcrypt

from app.config import settings

ALGORITHM = "HS256"


def hash_password(raw: str) -> str:
    return bcrypt.hashpw(raw.encode("utf-8"), bcrypt.gensalt()).decode("ascii")


def verify_password(raw: str, hashed: str) -> bool:
    if len(raw.encode("utf-8")) > 72:
        return False
    return bcrypt.checkpw(raw.encode("utf-8"), hashed.encode("ascii"))


def create_access_token(user_id: int) -> str:
    expire = datetime.now(UTC) + timedelta(
        minutes=settings.token_minutes
    )
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    return jwt.decode(
        token, settings.secret_key, algorithms=[ALGORITHM]
    )
