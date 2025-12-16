import pytest
from http import HTTPStatus


@pytest.mark.asyncio
async def test_add_book(session, client, token, author):
    response = await client.post(
        '/books/',
        json={
            'title': 'os sertoes',
            'year': 1902,
            'author_id': author.id,
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CREATED


@pytest.mark.asyncio
async def test_add_book_integrity_error(client, token, book):
    response = await client.post(
        '/books/',
        json={
            'title': book.title,
            'year': book.year,
            'author_id': book.author_id,
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
