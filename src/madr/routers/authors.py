from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from madr.users import current_active_user

from madr.schemas import AuthorSchemaCreate, AuthorSchemaGet
from madr.db import User, AsyncSession, get_async_session
from madr.models import Author

router = APIRouter(prefix='/authors', tags=['authors'])


T_Session = Annotated[AsyncSession, Depends(get_async_session)]


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=AuthorSchemaCreate
)
async def add_author(
    session: T_Session,
    author: AuthorSchemaCreate,
    user: User = Depends(current_active_user),
):
    new_author = Author(
        name=author.name,
    )

    session.add(new_author)
    await session.commit()
    await session.refresh(new_author)

    return new_author


@router.get('/', response_model=AuthorSchemaGet)
async def get_author_by_id(session: T_Session, author_id: int):
    author = await session.scalar(select(Author).where(Author.id == author_id))

    if not author:
        raise HTTPExeption(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Autor não consta no MADR.',
        )

    return author
