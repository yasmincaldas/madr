import pytest


@pytest.mark.asyncio
async def test_add_author(client, token):
    response = await client.post(
        '/authors/',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'Machado de Assis'},
    )

    assert response.json() == {'name': 'Machado de Assis'}
