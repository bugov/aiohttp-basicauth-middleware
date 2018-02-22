import hashlib
from http_basic_auth import generate_header

from example.server import get_app


async def test_no_auth_ok_url(aiohttp_server, aiohttp_client, loop):
    server = await aiohttp_server(get_app(loop))
    client = await aiohttp_client(server)

    response = await client.get('/hello')
    assert response.status == 200


async def test_fail_auth_no_header(aiohttp_server, aiohttp_client, loop):
    server = await aiohttp_server(get_app(loop))
    client = await aiohttp_client(server)

    response = await client.get('/admin/hello')
    assert response.status == 401


async def test_fail_auth_wrong(aiohttp_server, aiohttp_client, loop):
    server = await aiohttp_server(get_app(loop, {'test': 'secret'}))
    client = await aiohttp_client(server)

    response = await client.get(
        '/admin/hello',
        headers={'Authorization': generate_header('test', 'WRONG')},
    )
    assert response.status == 401


async def test_ok_auth(aiohttp_server, aiohttp_client, loop):
    server = await aiohttp_server(get_app(loop, {'test': 'secret'}))
    client = await aiohttp_client(server)

    response = await client.get(
        '/admin/hello',
        headers={'Authorization': generate_header('test', 'secret')},
    )
    assert response.status == 200


async def test_strategy(aiohttp_server, aiohttp_client, loop):
    server = await aiohttp_server(
        get_app(
            loop,
            {
                'test': '5f4dcc3b5aa765d61d8327deb882cf99',
            },
            lambda x: hashlib.md5(bytes(x, encoding='utf-8')).hexdigest(),
        )
    )
    client = await aiohttp_client(server)

    response = await client.get(
        '/admin/hello',
        headers={'Authorization': generate_header('test', 'password')},
    )
    assert response.status == 200
