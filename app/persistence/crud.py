from sqlalchemy.orm import Session

from app.schemas import AuthRequest
from . import models


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_token(db: Session, token: str):
    return db.query(models.User).filter(models.User.token == token).first()


def check_user_exist_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first() is not None


def create_user(db: Session, auth_request: AuthRequest, token: str, cookie: dict, freelancer_id: int):
    user = models.User(username=auth_request.username, token=token, cookie=cookie, freelancer_id=freelancer_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_cookie_by_username(db: Session, username: str, cookie: dict | None):
    user = get_user_by_username(db, username)
    if cookie is not None:
        user.cookie = cookie
    db.commit()
    db.refresh(user)
    return user

