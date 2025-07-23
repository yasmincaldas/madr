from sqlalchemy.orm import Mapped, mapped_column, registry, relationship
from sqlalchemy import ForeignKey

table_registry = registry()


@table_registry.mapped_as_dataclass
class Author:
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    books: Mapped[list['Book']] = relationship(
        'Book', 
        init=False, 
        back_populate='author', 
        cascade='all, delete-orphan') 



@table_registry.mapped_as_dataclass
class Book:
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    year: Mapped[int] 
    title: Mapped[str] = mapped_column(unique=True)
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'), nullable=False)

    author = Mapped[Author] = relationship('Author', init=False, back_populates='books') 