import fastapi
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import cat_schema, cat_crud
from api.database import database_connect as database

cat_router = APIRouter
cat_router = fastapi.APIRouter(
    prefix="/api/v1/auth/admin"
)


@cat_router.post("/create/cat", status_code=status.HTTP_201_CREATED, response_model=cat_schema.ReturnCat)
async def create_Category(create: cat_schema.CategoryCreate, db: Session = Depends(database.get_db)):
    result = cat_crud.check_name(db=db, name=create.name)
    if result:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category name already exist")
    create_catgory = cat_crud.create_cat(db=db, create_cat=create)
    return create_catgory


@cat_router.get("/get/cat/all", status_code=status.HTTP_201_CREATED)
async def get_all(db: Session = Depends(database.get_db)):
    result = cat_crud.get_all(db)
    return result


@cat_router.get("/get/cat/{cat_name}", status_code=status.HTTP_201_CREATED)
async def get_by_name(name: str, db: Session = Depends(database.get_db)):
    result = cat_crud.check_name(db, name)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist in database")
    cat_name = cat_crud.check_name(db, name)
    return cat_name


@cat_router.get("/get/{id}", status_code=status.HTTP_201_CREATED, response_model=cat_schema.ReturnCat)
async def get_by_id(id: int, db: Session = Depends(database.get_db)):
    result = cat_crud.get_cat_by_id(db, id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist in database")
    cat_id = cat_crud.get_cat_by_id(db, id)
    return cat_id


@cat_router.put("/update/{id}", status_code=status.HTTP_201_CREATED, response_model=cat_schema.ReturnCat)
async def update_category(id: int, update: cat_schema.CategoryUpdate, db: Session = Depends(database.get_db)):
    result = cat_crud.get_cat_by_id(db, id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist in database")
    update_category = cat_crud.update_cat(db, updated_post=update, cat_id=id)
    return update_category


@cat_router.delete(("/delete/{id}"), status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(id: int, db: Session = Depends(database.get_db)):
    result = cat_crud.get_cat_by_id(db, id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist in database")
    delete_category = cat_crud.delete_cat(db, cat_id=id)
    return ("Deleted")
