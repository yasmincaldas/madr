import factory
from madr.models import Author, Book
from madr.db import User


class UserFactory(factory.Factory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')


class AuthorFactory(factory.Factory):
    class Meta:
        model = Author

    name = factory.Sequence(lambda n: f'test{n}')


class BookFactory(factory.Factory):
    class Meta:
        model = Book

    year = factory.Sequence(lambda n: 1980 + n)
    title = factory.Sequence(lambda n: f'Book {n}')
    author_id = factory.Sequence(lambda n: n + 1)
