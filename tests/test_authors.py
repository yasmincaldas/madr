import pytest
from .factories import AuthorFactory
from http import HTTPStatus


@pytest.mark.asyncio
async def test_add_author(client, token):
    response = await client.post(
        '/authors/',
        json={'name': 'Machado de Assis'},
        headers={'Authorization': f'Bearer {token}'},
    )
    print(response.json())

    assert response.json() == {'name': 'Machado de Assis'}

@pytest.mark.asyncio
async def test_add_author_conflict_error(client, session, token, author):
    response = await client.post(
        '/authors/',
        json={'name': author.name},
        headers={'Authorization': f'Bearer {token}'},
    )
    print(response.json())

    assert response.status_code == HTTPStatus.CONFLICT

@pytest.mark.asyncio
async def test_get_author_by_id(client, session, token):
    author = AuthorFactory()

    session.add(author)
    await session.commit()
    await session.refresh(author)

    response = await client.get(
        f'/authors/{author.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert data['id'] == author.id
    assert data['name'] == author.name


@pytest.mark.asyncio
async def test_get_author_by_id_author_not_found_error(client, token):
    response = await client.get(
        f'/authors/999',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Autor não consta no MADR.'}


@pytest.mark.asyncio
async def test_delete_author_by_id(client, session, token):
    author = AuthorFactory()

    session.add(author)
    await session.commit()
    await session.refresh(author)

    response = await client.delete(
        f'/authors/{author.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK

