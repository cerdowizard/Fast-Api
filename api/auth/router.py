import re
from datetime import timedelta

from api import models
from api.database import database
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
                                                                                    detail="password must not be less "
                                                                                           "than 8 characters and "
                                                                                           "must contain one " 
                                                                                           "capital letter, "
                                                                                           "small letter and a symbol")
    db_user = crud.create_user(db=db, user=user)
    return db_user


@router.post('/login', response_model=schema.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not crypto.verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    # create a token
    # return token

    access_token = jwt_encoder.create_access_token(data={"user_id": user.id,
                                                         "role": user.role
                                                         })

    return {"access_token": access_token, "token_type": "bearer"}




