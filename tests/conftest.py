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
from madr.db import Base
from madr.db import User
from fastapi_users.password import PasswordHelper
from madr.db import Base, get_async_session
from madr.models import table_registry
from .factories import AuthorFactory


from fastapi_users.password import PasswordHelper


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(table_registry.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(table_registry.metadata.drop_all)


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
