from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from api.auth import crud
from api.adminActions import cat_crud, cat_schema
from api.database import database
from api.post import post_crud
from api.utils import jwt_encoder

adminRoute = APIRouter(
    prefix="/api/v1/auth/admin",
)


@adminRoute.get("/users/all", dependencies=[Depends(jwt_encoder.check_admin)])
async def get_all_user(db: Session = Depends(database.get_db)):
    users = crud.get_users(db=db)
    return users


@adminRoute.get("/posts/all", dependencies=[Depends(jwt_encoder.check_admin)])
async def get_all_posts(db: Session = Depends(database.get_db)):
    post = post_crud.get_all_posts(db=db)
    return post


@adminRoute.get("/category/all/", dependencies=[Depends(jwt_encoder.check_admin)])
async def get_all_category(db: Session = Depends(database.get_db)):
    category = cat_crud.get_all_category(db=db)
    return category


@adminRoute.post("/create/cat", status_code=status.HTTP_201_CREATED, response_model=cat_schema.ReturnCat,
                 dependencies=[Depends(jwt_encoder.check_admin)])
async def create_Category(create: cat_schema.CategoryCreate, db: Session = Depends(database.get_db)):
    result = cat_crud.check_name(db=db, name=create.name)
    if result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category name already exist")
    create_catgory = cat_crud.create_cat(db=db, create_cat=create)
    return create_catgory


@adminRoute.get("/get/cat/{cat_name}", status_code=status.HTTP_201_CREATED,
                dependencies=[Depends(jwt_encoder.check_admin)])
async def get_by_name(name: str, db: Session = Depends(database.get_db)):
    result = cat_crud.check_name(db, name)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist in database")
    cat_name = cat_crud.check_name(db, name)
    return cat_name


@adminRoute.get("/get/{id}", status_code=status.HTTP_201_CREATED, response_model=cat_schema.ReturnCat,
                dependencies=[Depends(jwt_encoder.check_admin)])
async def get_by_id(id: int, db: Session = Depends(database.get_db)):
    result = cat_crud.get_cat_by_id(db, id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist in database")
    cat_id = cat_crud.get_cat_by_id(db, id)
    return cat_id


@adminRoute.put("/update/admin/user/role/{id}")
async def update_role():
    pass


@adminRoute.put("/update/{id}", status_code=status.HTTP_201_CREATED, response_model=cat_schema.ReturnCat,
                dependencies=[Depends(jwt_encoder.check_admin)])
async def update_category(id: int, update: cat_schema.CategoryUpdate, db: Session = Depends(database.get_db)):
    result = cat_crud.get_cat_by_id(db, id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist in database")
    update_category = cat_crud.update_cat(db, updated_post=update, cat_id=id)
    return update_category


@adminRoute.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT,
                   dependencies=[Depends(jwt_encoder.check_admin)])
async def delete_category(id: int, db: Session = Depends(database.get_db)):
    result = cat_crud.get_cat_by_id(db, id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist in database")
    delete_category = cat_crud.delete_cat(db, cat_id=id)
    return ("Deleted")
