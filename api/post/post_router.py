import fastapi
from fastapi import Depends, HTTPException, status
from api.database.database import get_db
from sqlalchemy.orm import Session
from . import post_crud
from . import post_schema
from .. import models
from ..adminActions import cat_crud
from ..utils import jwt_encoder

post_router = fastapi.APIRouter(
    prefix="/api/v1/auth/post"
)


@post_router.get("/admin/get-all")
async def Get_All_Posts(db: Session = Depends(get_db), ):
    get_all_posts = post_crud.get_all_posts(db=db)
    return get_all_posts


@post_router.post("/", status_code=status.HTTP_201_CREATED)
def create_posts(post: post_schema.Post, db: Session = Depends(get_db),
                 current_user: int = Depends(jwt_encoder.get_current_user)):
    result = cat_crud.check_name(db, name=post.category)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist in database")
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


#

@post_router.get("/user/getbyid/{id}", status_code=201)
async def Get_Post_By_Id(post_id: int, db: Session = Depends(get_db)):
    result = post_crud.get_post_by_id(db, post_id=post_id)
    if not result:
        raise HTTPException(status_code=404, detail="Post not found")
    return result


@post_router.put("/user/update/{id}", status_code=status.HTTP_201_CREATED)
async def Update_By_Id(id: int, updated_post: post_schema.PostUpdate, db: Session = Depends(get_db)):
    result = cat_crud.check_name(db, name=updated_post.category)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category does not exist in database")

    post_check = post_crud.get_post_by_id(db=db, post_id=id)
    if not post_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post_query = post_crud.update_article(db=db, post_id=id, updated_post=updated_post)
    return post_query


@post_router.delete("/user/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def Delete_By_Id(id: int, db: Session = Depends(get_db)):
    result = post_crud.get_post_by_id(db=db, post_id=id)
    if not result:
        raise HTTPException(status_code=404, detail="Post not found")
    return post_crud.delete_post(db=db, post_id=id)
