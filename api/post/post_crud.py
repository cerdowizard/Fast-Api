from sqlalchemy.orm import Session
from .. import models
from . import post_schema
from api.utils import crypto, jwt_encoder


def create_post(db: Session, post: post_schema.Post):
    create_post = models.Post(
        owner_id=jwt_encoder.get_current_user,
        **post.dict()
    )
    db.add(create_post)
    db.commit()
    db.refresh(create_post)
    return create_post


def get_all_posts(db: Session):
    return db.query(models.Post).all()


def check_name(db: Session, name: str):
    return db.query(models.Category).filter(models.Category.name == name).first()


def get_post_by_id(db: Session, post_id: int):
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def update_article(db: Session, post_id: int, updated_post: post_schema.PostUpdate):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


def delete_post(db: Session, post_id: int):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    post.delete(synchronize_session=False)
    db.commit()
