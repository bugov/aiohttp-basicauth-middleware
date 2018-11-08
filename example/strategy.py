import asyncio
from aiohttp import web
from aiohttp_basicauth_middleware import basic_auth_middleware
from aiohttp_basicauth_middleware.strategy import BaseStrategy


class SkipOptionsStrategy(BaseStrategy):
    async def check(self):
        if self.request.method == 'OPTIONS':
            return await self.handler(self.request)

        return await super().check()


def hello(request):
    return web.Response(text='Hello')


async def world(request):
    return web.Response(text='world')


def get_app(loop, auth_dict=None):
    if auth_dict is None:
        auth_dict = {}

    app = web.Application(loop=loop)
    app.router.add_route('*', '/admin/hello', hello)
    app.router.add_route('*', '/admin/world', world)

    app.middlewares.append(
        basic_auth_middleware(('/admin',), auth_dict, SkipOptionsStrategy)
    )

    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    web.run_app(get_app(loop))
