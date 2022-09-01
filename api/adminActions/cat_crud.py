from api.adminActions import cat_schema
from sqlalchemy.orm import Session
from api import models


def create_cat(create_cat: cat_schema.CategoryCreate, db=Session):
    create_cat = models.Category(
        **create_cat.dict()
    )
    db.add(create_cat)
    db.commit()
    db.refresh(create_cat)
    return create_cat


def check_name(db: Session, name: str):
    return db.query(models.Category).filter(models.Category.name == name).first()


def get_cat_by_id(db: Session, cat_id: int):
    return db.query(models.Category).filter(models.Category.id == cat_id).first()


def get_all(db: Session):
    return db.query(models.Category).all()


def update_cat(db: Session, cat_id: int, updated_post: cat_schema.CategoryUpdate):
    cat_query = db.query(models.Category).filter(models.Category.id == cat_id)
    cat_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return cat_query.first()


def delete_cat(db: Session, cat_id: int):
    cat = db.query(models.Category).filter(models.Category.id == cat_id)
    cat.delete(synchronize_session=False)
    db.commit()
