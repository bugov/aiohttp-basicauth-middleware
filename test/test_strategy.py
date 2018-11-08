from http_basic_auth import generate_header

from example.strategy import get_app


async def test_skip_options_check(aiohttp_server, aiohttp_client, loop):
    server = await aiohttp_server(get_app(loop))
    client = await aiohttp_client(server)

    response = await client.options('/admin/hello')
    assert response.status == 200

    response = await client.get('/admin/hello')
    assert response.status == 401


async def test_pass(aiohttp_server, aiohttp_client, loop):
    server = await aiohttp_server(get_app(loop, {'user': 'secret'}))
    client = await aiohttp_client(server)

    response = await client.get(
        '/admin/hello',
        headers={'Authorization': generate_header('user', 'secret')},
    )
    assert response.status == 200

    response = await client.get(
        '/admin/world',
        headers={'Authorization': generate_header('user', 'secret')},
    )
    assert response.status == 200

    response = await client.get(
        '/admin/hello',
        headers={'Authorization': generate_header('user', 'pass')},
    )
    assert response.status == 401
