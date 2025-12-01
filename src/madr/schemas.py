from pydantic import BaseModel, Field, validator
import uuid
from typing import Annotated
from fastapi_users import schemas
from madr.utils import sanitize_string
from madr.models import Book


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class BookSchemaCreate(BaseModel):
    year: int
    title: str
    author_id: int


class AuthorSchemaBase(BaseModel):
    name: str

    @validator("name")
    def sanitize_name(cls, v):
        return sanitize_string(v)


class AuthorSchemaGet(AuthorSchemaBase):
    id: int


class AuthorSchemaCreate(AuthorSchemaBase):
    pass


class Message(BaseModel):
    message: str

class AuthorSchemaPublic(AuthorSchemaBase):
    id: int

class AuthorSchemaDelete():
    pass


class AuthorSchemaFilter(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    tags: list[str] = []
