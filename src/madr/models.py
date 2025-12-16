from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    registry,
    relationship,
    DeclarativeBase,
)
from fastapi_users.db import (
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    books: Mapped[list['Book']] = relationship(
        back_populates='author', cascade='all, delete-orphan'
    )


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int]
    title: Mapped[str] = mapped_column(unique=True)

    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'))
    author: Mapped['Author'] = relationship(back_populates='books')
