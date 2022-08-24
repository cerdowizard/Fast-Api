from typing import Optional

from pydantic import BaseModel, Field


class Post(BaseModel):
    title: str = Field(..., example="Post title")
    short_desc: str = Field(..., example="Short description about the content")
    content: str = Field(..., example="In publishing and graphic design, Lorem ipsum is a placeholder text commonly "
                                      "used to demonstrate the visual form of a document or a typeface without")
    category: str = Field(..., example="Category name")
    author: str = Field(..., example="First Last")
    imageUrl: str = Field(..., eample="http://localhost/image/url")


class PostUpdate(Post):
    title: Optional[str]
    short_desc: str = Field(..., example="Short description about the content")
    content: str = Field(..., example="In publishing and graphic design, Lorem ipsum is a placeholder text commonly "
                                      "used to demonstrate the visual form of a document or a typeface without")
    category: str = Field(..., example="Category name")
    author: str = Field(..., example="First Last")
    imageUrl: str = Field(..., eample="http://localhost/image/url")

    class Config:
        orm_mode = True
