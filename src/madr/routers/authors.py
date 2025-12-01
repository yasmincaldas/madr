from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from madr.users import current_active_user

from madr.schemas import AuthorSchemaCreate, AuthorSchemaGet, Message, AuthorSchemaPublic, AuthorSchemaBase
from madr.db import User, AsyncSession, get_async_session
from madr.models import Author

from sqlalchemy import select


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

    author_db = await session.scalar(select(Author).where(Author.name == author.name))

    if author_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Esse autor já consta no MADR.'
        )

    new_author = Author(
        name=author.name
    )

    session.add(new_author)
    await session.commit()
    await session.refresh(new_author)

    return new_author


@router.get('/{author_id}', response_model=AuthorSchemaGet)
async def get_author_by_id(
    session: T_Session, 
    author_id: int,
    user: User = Depends(current_active_user),
    ):

    author = await session.scalar(select(Author).where(Author.id == author_id))

    if not author:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Autor não consta no MADR.',
        )

    return author


@router.delete('/{author_id}', response_model=Message)
async def delete_author_by_id(
    session: T_Session, 
    author_id: int,
    user: User = Depends(current_active_user),
    ):

    author_db = await session.scalar(select(Author).where(Author.id == author_id))

    if not author_db:
        raise HTTPException(
            status_code= HTTPStatus.NOT_FOUND,
            detail='Autor não consta no MADR.'
        )

    session.delete(author_db)
    await session.commit()

    return {'message': f'O autor {author_db.name} foi deletado.'}

@router.patch('/{author_id}', response_model=AuthorSchemaPublic)
async def patch_author(
    session: T_Session, 
    author_id: int, 
    author: AuthorSchemaBase,
    user: User = Depends(current_active_user),
    ):

    author_db = await session.scalar(select(Author).where(Author.id == author_id))

    if not author_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Autor não consta no MADR.'
        )

    author_db.name = author.name
    
    session.add(author_db)
    await session.commit()
    await session.refresh(author_db)
    return author_db


