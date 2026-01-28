from http import HTTPStatus
from typing import Annotated, Union

from fastapi import APIRouter, Depends, HTTPException
from madr.users import current_active_user

from madr.schemas import (
    BookSchemaCreate,
    BookSchemaBase,
    BookSchemaGet,
    BookSchemaList,
    BookSchemaPublic,
    BookSchemaUpdate,
    Message,
)
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


@router.get('/{book_id}', response_model=BookSchemaGet)
async def get_book_by_id(
    session: T_Session, book_id: int, user: User = Depends(current_active_user)
):
    book = await session.scalar(select(Book).where(Book.id == book_id))

    if not book:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Livro não consta no MADR.',
        )

    return book


@router.get('/', response_model=BookSchemaList)
async def get_books(
    session: T_Session,
    title: Union[str, None] = None,
    year: Union[int, None] = None,
    offset: int | None = 0,
    limit: int | None = 20,
):
    query = select(Book)

    if title:
        query = query.filter(Book.title.contains(title))

    if year:
        query = query.filter(Book.year == year)

    books = await session.scalars(query.offset(offset).limit(limit))

    return {'books': books.all()}


@router.patch('/{book_id}', response_model=BookSchemaPublic)
async def patch_book(
    session: T_Session,
    book_id: int,
    book: BookSchemaUpdate,
    user: User = Depends(current_active_user),
):
    book_db = await session.scalar(select(Book).where(Book.id == book_id))

    if not book_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Livro não consta no MADR'
        )

    for key, value in book.model_dump(exclude_unset=True).items():
        if key == 'title':
            book_title_db = await session.scalar(
                select(Book).where(Book.title == value)
            )

            if book_title_db:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail='Esse livro já consta no MADR',
                )
            setattr(book_db, key, value)
        elif key == 'author_id':
            author_db = await session.scalar(
                select(Author).where(Author.id == book.author_id)
            )

            if not author_db:
                raise HTTPException(
                    status_code=HTTPStatus.CONFLICT,
                    detail='Esse autor não consta no MADR',
                )
            setattr(book_db, key, value)
        else:
            setattr(book_db, key, value)

    session.add(book_db)
    session.commit()
    session.refresh(book_db)

    return book_db


@router.delete('/{book_id}', response_model=Message)
async def delete_book(
    session: T_Session,
    book_id: int,
    user: User = Depends(current_active_user),
):
    book_db = await session.scalar(select(Book).where(Book.id == book_id))

    if not book_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Esse livro não consta no MADR',
        )

    await session.delete(book_db)
    await session.commit()

    return {'message': f'O livro {book_db.title} foi deletado'}
