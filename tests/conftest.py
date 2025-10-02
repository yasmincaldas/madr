import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from httpx import ASGITransport, AsyncClient
from sqlalchemy.pool import StaticPool
from madr.app import app
from madr.db import Base
from madr.db import User
from fastapi_users.password import PasswordHelper


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(
        'sqlite+aiosqlite:///./test_database.db',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client(session):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='http://test'
    ) as client:
        yield client


@pytest_asyncio.fixture
async def verified_user(session):
    password_helper = PasswordHelper()
    hashed_password = password_helper.hash('testpassword')  

    user = User(
        email='verifieduser@test.com',
        hashed_password=hashed_password,  
        is_active=True,
        is_verified=True,
        is_superuser=False,
    )


    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest_asyncio.fixture
async def token(client, verified_user):
    response = await client.post(
        '/auth/jwt/login',
        data={
            'username': verified_user.email,  
            'password': 'testpassword'        
        }
    )

    return response.json()["access_token"]

