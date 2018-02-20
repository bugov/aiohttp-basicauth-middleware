import hashlib
import sys
from basicauth import encode

sys.path.append('.')

from example.server import get_app


def test_no_auth_ok_url(aiohttp_server, aiohttp_client, loop):
    async def test():
        server = await aiohttp_server(get_app(loop))
        client = await aiohttp_client(server)

        response = await client.get('/hello')
        assert response.status == 200

    loop.run_until_complete(test())


def test_fail_auth_no_header(aiohttp_server, aiohttp_client, loop):
    async def test():
        server = await aiohttp_server(get_app(loop))
        client = await aiohttp_client(server)

        response = await client.get('/admin/hello')
        assert response.status == 401

    loop.run_until_complete(test())


def test_fail_auth_wrong(aiohttp_server, aiohttp_client, loop):
    async def test():
        server = await aiohttp_server(get_app(loop, {'test': 'secret'}))
        client = await aiohttp_client(server)

        response = await client.get(
            '/admin/hello',
            headers={'Authorization': encode('test', 'WRONG')},
        )
        assert response.status == 401

    loop.run_until_complete(test())


def test_ok_auth(aiohttp_server, aiohttp_client, loop):
    async def test():
        server = await aiohttp_server(get_app(loop, {'test': 'secret'}))
        client = await aiohttp_client(server)

        response = await client.get(
            '/admin/hello',
            headers={'Authorization': encode('test', 'secret')},
        )
        assert response.status == 200

    loop.run_until_complete(test())


def test_strategy(aiohttp_server, aiohttp_client, loop):
    async def test():
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
            headers={'Authorization': encode('test', 'password')},
        )
        assert response.status == 200

    loop.run_until_complete(test())
