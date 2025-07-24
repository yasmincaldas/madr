from pydantic import BaseModel, Field
import uuid
from typing import Annotated
from fastapi_users import schemas
from madr.utils import sanitize_string


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

    @field_validator('title')
    @classmethod
    def sanitize_title(cls, title: str) -> str:
        return sanitize_string(title)


class AuthorSchemaCreate(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=100)]

    @field_validator('name')
    @classmethod
    def sanitize_name(cls, name: str) -> str:
        return sanitize_string(name)
