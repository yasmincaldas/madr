import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_session,
    async_sessionmaker,
)
from httpx import ASGITransport, AsyncClient
from sqlalchemy.pool import StaticPool
from madr.app import app
from madr.models import Base, User, Book
from fastapi_users.password import PasswordHelper
from madr.db import Base, get_async_session
from .factories import AuthorFactory, BookFactory
from madr.settings import Settings

from fastapi_users.password import PasswordHelper


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(Settings().DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(autouse=True)
async def override_get_async_session(session):
    async def _override():
        yield session

    app.dependency_overrides[get_async_session] = _override
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://testserver'
    ) as ac:
        yield ac


@pytest_asyncio.fixture
async def user(session):
    hashed_password = PasswordHelper().hash('test')

    user = User(
        email='myuser@test.com',
        hashed_password=hashed_password,
        is_active=True,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest_asyncio.fixture
async def token(client, user):
    data = {
        'username': 'myuser@test.com',
        'password': 'test',
    }
    response = await client.post(
        '/auth/jwt/login',
        data=data,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
    )

    data = response.json()
    print(data)
    return response.json()['access_token']


@pytest_asyncio.fixture
async def author(session):
    author = AuthorFactory(name='test author')
    session.add(author)
    await session.commit()
    await session.refresh(author)

    return author


@pytest_asyncio.fixture
async def book(session, author):
    book = Book(year=1854, title='walden', author_id=author.id)

    session.add(book)
    await session.commit()
    await session.refresh(book)

    return book
