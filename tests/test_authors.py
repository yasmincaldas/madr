import pytest


@pytest.mark.asyncio
async def test_add_author(client, token):
    response = await client.post(
        '/authors/',
        json={'name': 'Machado de Assis'},
        headers={'Authorization': f'Bearer {token}'},
    )
    print(response.json())

    assert response.json() == {'name': 'Machado de Assis'}
    
