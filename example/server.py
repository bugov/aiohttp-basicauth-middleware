import asyncio
from aiohttp import web
from aiohttp_basicauth_middleware import basic_auth_middleware


def hello(request):
    return web.Response(text='Hello')


def get_app(loop, auth_dict=None, strategy=lambda x: x):
    if auth_dict is None:
        auth_dict = {}

    app = web.Application(loop=loop)

    app.router.add_route('GET', '/hello', hello)
    app.router.add_route('GET', '/admin/hello', hello)

    app.middlewares.append(
        basic_auth_middleware(('/admin',), auth_dict, strategy)
    )

    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    web.run_app(get_app(loop))
