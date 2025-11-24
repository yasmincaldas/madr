import pytest
from .factories import AuthorFactory


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
async def test_get_author_by_id(client, session, token):
    author = AuthorFactory()

    session.add(author)
    await session.commit()
    await session.refresh(author)

    response = await client.get(
        f'/authors/?author_id={author.id}',  
        headers={'Authorization': f'Bearer {token}'},
    )


    assert response.status_code == 200
    data = response.json()
    assert data["id"] == author.id
    assert data["name"] == author.name