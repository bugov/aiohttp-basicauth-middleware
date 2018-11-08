from example.strategy import get_app


async def test_skip_options_check(aiohttp_server, aiohttp_client, loop):
    server = await aiohttp_server(get_app(loop))
    client = await aiohttp_client(server)

    response = await client.options('/admin/hello')
    assert response.status == 200

    response = await client.get('/admin/hello')
    assert response.status == 401
