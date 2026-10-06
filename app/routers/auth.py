from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.auth import Token, UserCreate, UserRead
from app.security import create_access_token
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

DB = Annotated[Session, Depends(get_db)]


def get_service(db: DB) -> AuthService:
    return AuthService(db)


Service = Annotated[AuthService, Depends(get_service)]


@router.post("/register", response_model=UserRead, status_code=201)
def register(body: UserCreate, service: Service):
    return service.register(body)


@router.post("/login", response_model=Token)
def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Service,
):
    user = service.authenticate(form.username, form.password)
    token = create_access_token(user.id)
    return Token(access_token=token)