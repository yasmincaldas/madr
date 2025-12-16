from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from madr.users import current_active_user

from madr.schemas import BookSchemaCreate, BookSchemaBase
from madr.db import User, AsyncSession, get_async_session
from madr.models import Book

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError


router = APIRouter(prefix='/books', tags=['books'])


T_Session = Annotated[AsyncSession, Depends(get_async_session)]


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=BookSchemaCreate
)
async def add_book(
    session: T_Session,
    book: BookSchemaBase,
    user: User = Depends(current_active_user),
):
    book_db = await session.scalar(
        select(Book).where(Book.title == book.title)
    )

    if book_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Esse livro já existe'
        )

    new_book = Book(year=book.year, title=book.title, author_id=book.author_id)

    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)

    return new_book
