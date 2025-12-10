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
    book_db = Book(**book.model_dump())

    try:
        session.add(book_db)
        await session.commit()
        await session.refresh(book_db)

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Esse livro já existe'
        )

    return book_db
