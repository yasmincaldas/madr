import factory
from madr.models import Author
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
