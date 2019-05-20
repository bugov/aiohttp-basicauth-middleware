from aiohttp import web

from aiohttp_basicauth_middleware import basic_auth_middleware
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


async def test_no_strategy(aiohttp_server, aiohttp_client, loop):
    async def public_view(request):
        return web.Response(text='Public view')

    async def secret_view(request):
        return web.Response(text='Secret view')

    app = web.Application()
    app.router.add_route('GET', '/public', public_view)
    app.router.add_route('GET', '/secret', secret_view)
    app.middlewares.append(
        basic_auth_middleware(
            ('/secret',),
            {'user': 'password'},
        )
    )

    server = await aiohttp_server(app)
    client = await aiohttp_client(server)

    response = await client.get('/public')
    assert response.status == 200

    response = await client.get('/secret')
    assert response.status == 401

    response = await client.get(
        '/secret',
        headers={'Authorization': generate_header('user', 'password')},
    )
    assert response.status == 200
