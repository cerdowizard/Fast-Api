from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class BaseUser(BaseModel):
    email: EmailStr = Field(..., example="example@gmail.com")
    username: str = Field(..., example="example01")
    role: Optional[str]


class UserSchema(BaseUser):
    cn_password: str = Field(..., example="example@1.")
    password: str = Field(..., example="example@1.")


class UserPassword(BaseUser):
    password: str


class UserForgotPassword(BaseModel):
    email: str

    class Config:
        orm_mode = True


class ReturnUser(BaseUser):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(Token):
    id:int
