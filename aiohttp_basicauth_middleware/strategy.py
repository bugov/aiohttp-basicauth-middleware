import asyncio
from typing import Callable, Tuple
import logging

from aiohttp import web
from http_basic_auth import parse_header, BasicAuthException

log = logging.getLogger(__name__)


class BaseStrategy:
    def __init__(self, request: web.Request, storage: dict, handler: Callable, header: str):
        self.request = request
        self.storage = storage
        self.handler = handler
        self.header = header

        log.debug('Init strategy %r', (self.request, self.storage, self.handler))

    def get_credentials(self) -> Tuple[str, str]:
        try:
            return parse_header(self.header)
        except BasicAuthException:
            log.info('Invalid basic auth header: %r', self.header)
            self.on_error()

    async def password_test(self) -> bool:
        login, password = self.get_credentials()
        server_password = self.storage.get(login)

        if server_password != password:
            return False

        return True

    async def check(self) -> web.Response:

        if await self.password_test():
            return await self.handler(self.request)

        self.on_error()

    def on_error(self):
        raise web.HTTPUnauthorized(headers={'WWW-Authenticate': 'Basic'})
