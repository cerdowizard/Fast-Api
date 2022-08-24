from fastapi import APIRouter, Depends, HTTPException, status

from api.database import database_connect as database
from sqlalchemy.orm import Session
from ..models import User
from ..utils import jwt_encoder

user_router = APIRouter(
    prefix="/api/v1/auth"
)


@user_router.post("/admin/create")
async def create_user():
    pass


@user_router.get("/admin/all/users")
async def get_all_users():
    pass


@user_router.get("/get/user{id}")
async def get_user():
    pass


@user_router.put("/update/admin/user/role/{id}")
async def update_role():
    pass


@user_router.put("/update/user/{id}")
async def update_user():
    pass


@user_router.delete("/delete/user/{id}")
async def delete_user():
    pass


# @user_router.get("/users/me/")
# async def read_users_me(current_user: User = Depends(jwt_encoder.check_active), db: Session = Depends(database.get_db)):
#     return current_user
