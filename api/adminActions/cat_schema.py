from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class CategoryUpdate(BaseModel):
    name: str

    class Config:
        orm_mode = True


class ReturnCat(CategoryBase):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    class Config:
        orm_mode = True
