import re
from datetime import timedelta

from api.database import database_connect as database
from sqlalchemy.orm import Session
import fastapi
from fastapi import Depends, HTTPException, status
from api.auth import schema, crud
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from api.utils import crypto, jwt_encoder, constant
import uuid

router = fastapi.APIRouter(
    prefix="/api/v1/auth"
)


@router.post("/register", response_model=schema.ReturnUser, status_code=201)
async def register(user: schema.UserSchema, db: Session = Depends(database.get_db)):
    result = crud.get_user_by_email(db, email=user.email)
    if result:
        raise HTTPException(status_code=400, detail="Email already exist")

    if user.password != user.cn_password:
        raise HTTPException(status_code=400, detail="password and confirm password must be the same")

    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail="password must not be less than 8 characters and must contain one "
                                                    "capital letter, small letter and a symbol ")
    if re.fullmatch(r'[A-Za-z0-9@#$%^&+=]{8,}', user.password): raise HTTPException(status_code=400,
                                                                                    detail="password must not be less than 8 characters and must contain one " "capital letter, small letter and a symbol")
    db_user = crud.create_user(db=db, user=user)
    return db_user


@router.post("/login", status_code=status.HTTP_201_CREATED, response_model=schema.TokenData)
async def login(db: Session = Depends(database.get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = crud.get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=404, detail="User doesn't exist")

    # verify password
    check_pass = crypto.verify_password(form_data.password, user.password)
    if not check_pass:
        raise HTTPException(status_code=404, detail="Invalid password")

    access_token_expires = timedelta(minutes=constant.ACCESS_TOKEN_EXPIRE_TIME)
    token = await jwt_encoder.create_access_token(data={"user_id": user.id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_info": {
            "id": user.id,
            "email": user.username,
        }
    }

# @router.get("/admin/all/users")
# async def get_all_user(db: Session = Depends(database.get_db), ):
#     users = crud.get_users(db=db)
#     return users

# @router.get("/users/admin", dependencies=[Depends(jwt_encoder.check_admin)])
# async def get_all_user(db: Session = Depends(database.get_db)):
#     users = crud.get_users(db=db)
#     return users

# @router.get("/users/admin", dependencies=[Depends(jwt_encoder.check_admin)])
# async def get_all_user(db: Session = Depends(database.get_db)):
#     users = crud.get_users(db=db)
#     return users
# #
#
# @router.post("/forgot-password", status_code=201)
# async def forgot_password(request: schema.UserForgotPassword, db: Session = Depends(database.get_db)):
#     result = crud.get_user_by_email(db, request.email)
#     if not result:
#         raise HTTPException(status_code=400, detail="Email does not exist in database")
#
#     rest_code = uuid.uuid1()
#     await crud.create_reset_token(request.email, rest_code.rest_code)
#     return rest_code
