from sqlalchemy.orm import Session
from api.utils import crypto
from . import schema
from .. import models


def create_user(db: Session, user: schema.UserSchema):
    hashed_password = crypto.hash_password(user.password)
    db_user = models.User(
        email=user.email,
        username=user.email,
        password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_reset_token(db: Session, email: str, rest_code):
    db_token = models.Token(
        **rest_code.dict()
    )
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()
