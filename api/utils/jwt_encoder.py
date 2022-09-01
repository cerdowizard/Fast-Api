from datetime import datetime, timedelta
from jose import JWTError, jwt
from api.auth import schema
from api.database import database
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from api import models
from api.models import User
from api.utils import constant
from api.utils.constant import ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/v1/auth/login')


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=constant.ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, constant.SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:

        payload = jwt.decode(token, constant.SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schema.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user





def decode_token(access_token: str):
    claims = jwt.decode(access_token, key=constant.SECRET_KEY, algorithms=constant.ALGORITHM)
    if not claims:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, )
    return claims


def check_active(access_token: str = Depends(oauth2_scheme)):
    claims = decode_token(access_token)
    if claims.get("user_id"):
        return claims
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED_User",
                        headers={"WWW-Authenticate": "Bearer"})


def check_admin(claims: dict = Depends(check_active)):
    role = claims.get("role")
    if role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="UNAUTHORIZED_Admin",
                            headers={"WWW-Authenticate": "Bearer"})
    return claims


def user_role_check(token: str = Depends(oauth2_scheme)):
    claims = verify_access_token(token)
    if claims.get("role"):
        return claims
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="UNAUTHORIZED_User",
                        headers={"WWW-Authenticate": "Bearer"})
    return claims


