from pydantic import BaseModel, Field, validator, ConfigDict
import uuid
from typing import Annotated, List
from fastapi_users import schemas
from madr.utils import sanitize_string
from madr.models import Book


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


class BookSchemaBase(BaseModel):
    year: int
    title: str
    author_id: int

    @validator('title')
    def sanitize_name(cls, v):
        return sanitize_string(v)


class BookSchemaCreate(BookSchemaBase):
    id: int


class BookSchemaGet(BookSchemaBase):
    id: int


class BookSchemaPublic(BookSchemaBase):
    id: int


class BookSchemaUpdate(BaseModel):
    ano: int | None = None
    titulo: str | None = None
    romancista_id: int | None = None


class BookSchemaList(BaseModel):
    books: List[BookSchemaBase] = Field(default_factory=list)


class AuthorSchemaBase(BaseModel):
    name: str

    @validator('name')
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


class AuthorSchemaDelete:
    pass


class AuthorSchemaList(BaseModel):
    authors: list[AuthorSchemaPublic] = []

    model_config = ConfigDict(from_attributes=True)
