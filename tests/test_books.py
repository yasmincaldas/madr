import pytest
from http import HTTPStatus
from .factories import BookFactory


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


@pytest.mark.asyncio
async def test_get_book_by_id(client, token, book):
    response = await client.get(
        f'/books/{book.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['id'] == book.id

@pytest.mark.asyncio
async def test_get_book_by_id_not_found_error(client, token):
    response = await client.get(
        f'/books/999',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.asyncio
async def test_get_books_filter_by_title(client, session, author, token):
    books = BookFactory.create_batch(5, author_id=author.id)
    book = books[0]
    book.title = 'carta sobre a felicidade'
    session.add_all(books)
    await session.commit()

    response = await client.get(
        '/books/?title=fe',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()
    print(data)

    assert response.status_code == HTTPStatus.OK



@pytest.mark.asyncio
async def test_get_books_filter_by_year(client, session, author, token):
    books = BookFactory.create_batch(5, author_id=author.id)
    book = books[0]
    book.year = 1985
    session.add_all(books)
    await session.commit()

    response = await client.get(
        f'/books/?year={book.year}',
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()
    print(data)

    assert response.status_code == HTTPStatus.OK
