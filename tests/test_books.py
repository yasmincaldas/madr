import pytest
from .factories import BookFactory
from http import HTTPStatus


@pytest.mark.asyncio
async def test_add_book(session, client, token):
    book = BookFactory()
    session.add(book)
    await session.commit()
    await session.refresh(book)

    response = await client.post(
        '/books/',
        json={
            'title': book.title,
            'year': book.year,
            'author_id': book.author_id,
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED
