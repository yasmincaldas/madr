import pytest
from madr.db import User
from madr.models import Author
from sqlalchemy import select


@pytest.mark.asyncio
async def test_create_user_db(session):
    user = User(email='test@gmail.com', hashed_password='mypassword')

    session.add(user)
    await session.commit()

    result = await session.scalar(
        select(User).where(User.email == 'test@gmail.com')
    )

    assert result.email == 'test@gmail.com'


@pytest.mark.asyncio
async def test_create_author_db(session):
    user = Author(
        name='exemple',
    )

    session.add(user)
    await session.commit()

    result = await session.scalar(
        select(Author).where(Author.name == 'exemple')
    )

    assert result.name == 'exemple'
