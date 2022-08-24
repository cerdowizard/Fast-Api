import jwt
from datetime import datetime, timedelta
from jose import JWTError, jwt
from api.auth import schema
from api.auth.schema import TokenData
from api.database import database_connect as database
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from api import models
from api.models import User
from api.utils import constant
from api.utils.constant import ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')


async def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=constant.ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, constant.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(access_token: str, credentials_exception):
    try:
        payload = jwt.decode(access_token, key=constant.SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            credentials_exception

    except JWTError:
        credentials_exception
        return id


def get_current_user(access_token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    access_token = decode_token(access_token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == access_token.id).first()
    return user

# def verify_access_token(access_token: str):
#     payload = jwt.decode(access_token, SECRET_KEY, algorithms=constant.ALGORITHM)
#     if not payload:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED_User",
#                             headers={"WWW""-Authenticate": "Bearer"})


# def current_user(access_token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
#     payload = decode_token(access_token)
#
#     if not payload:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED_User",
#                             headers={"WWW""-Authenticate": "Bearer"})
#
#
# def check_admin(payload: dict = Depends(current_user)):
#     role = payload.get("user.role")
#     if role is not "admin":
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail="UNAUTHORIZED_Admin",
#                             headers={"WWW-Authenticate": "Bearer"})
#     return payload

#
#


# def get_current_user(access_token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
#     credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                                           detail="UNAUTHORIZED_Admin",
#                                           headers={"WWW-Authenticate": "Bearer"})
#     return verify_access_token(access_token, credentials_exception)

# def check_active(access_token: str = Depends(oauth2_scheme)):
#     claims = decode_token(access_token)
#     if claims.get("is_active"):
#         return claims
#     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED_User",
#                         headers={"WWW-Authenticate": "Bearer"})

#
#
#
#
#
# payload = jwt.decode(access_token, key=constant.SECRET_KEY, algorithms=constant.ALGORITHM)
# id: str = payload.get("user.role", "user.id")
# if not payload:
#     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cannot validate user")
# return payload
#
#
#
# async def create_access_token(data: dict, expires_delta: timedelta | None = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=constant.ALGORITHM)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, constant.SECRET_KEY, algorithm=constant.ALGORITHM)
#     return encoded_jwt
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, constant.SECRET_KEY, algorithms=constant.ALGORITHM)
#         id: int = payload.get("sub")
#         if id is None:
#             raise credentials_exception
#         token_data = TokenData(id=id)
#     except JWTError:
#         raise credentials_exception
#     user = db.query(models.User).filter(models.User.id == token_data.id).first()
#     if user is None:
#         raise credentials_exception
#     return user
#
#
# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user
#
#
# async def check_user_role(current_user: User = Depends(get_current_user)):
#     if current_user.role == "admin":
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#         )
# #


# async def create_access_token(user: models.User):
#     claims = {
#         "user_id": user.id,
#         "email": user.email,
#         "role": user.role,
#         "is_active": user.is_active,
#         "exp": datetime.utcnow() + timedelta(minutes=constant.ACCESS_TOKEN_EXPIRE_TIME)
#     }
#     return jwt.encode(claims,
#                       key=constant.SECRET_KEY,
#                       algorithm=constant.ALGORITHM)
#
#
# def decode_token(access_token: str):
#     claims = jwt.decode(access_token, key=constant.SECRET_KEY, algorithms=constant.ALGORITHM)
#     if not claims:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, )
#     return claims
#
#
# def check_active(access_token: str = Depends(oauth2_scheme)):
#     claims = decode_token(access_token)
#     if claims.get("user_id"):
#         return claims
#     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED_User",
#                         headers={"WWW-Authenticate": "Bearer"})
#
#
#
# def check_admin(claims: dict = Depends(check_active)):
#     role = claims.get("role")
#     if role != "admin":
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                             detail="UNAUTHORIZED_Admin",
#                             headers={"WWW-Authenticate": "Bearer"})
#     return claims
