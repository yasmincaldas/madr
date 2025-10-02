from pydantic import BaseModel, Field
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


class AuthorSchemaGet(AuthorSchemaBase):
    id: int


class AuthorSchemaCreate(AuthorSchemaBase):
    pass


class AuthorSchemaUpdate(AuthorSchemaBase):
    pass
