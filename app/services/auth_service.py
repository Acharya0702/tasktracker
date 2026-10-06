from sqlalchemy import select
from sqlalchemy.orm import Session

from app.errors import ConflictError, UnauthorizedError
from app.models.user import User
from app.schemas.auth import UserCreate
from app.security import hash_password, verify_password


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, data: UserCreate) -> User:
        existing = self.db.scalar(
            select(User).where(User.email == data.email)
        )
        if existing:
            raise ConflictError("Email already registered")

        user = User(
            email=data.email,
            name=data.name,
            password_hash=hash_password(data.password),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate(self, email: str, password: str) -> User:
        user = self.db.scalar(
            select(User).where(User.email == email)
        )
        if user is None or not verify_password(password, user.password_hash):
            raise UnauthorizedError("Invalid email or password")
        return user