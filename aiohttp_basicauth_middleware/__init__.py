import inspect
import logging
from typing import (
    Callable,
    Iterable,
    Type,
    Coroutine,
)

from aiohttp import web
from http_basic_auth import parse_header, BasicAuthException
from aiohttp_basicauth_middleware.strategy import BaseStrategy


log = logging.getLogger(__name__)


def check_access(
    auth_dict: dict,
    header_value: str,
    strategy: Callable = lambda x: x
) -> bool:
    log.debug('Check access: %r', header_value)

    try:
        login, password = parse_header(header_value)
    except BasicAuthException:
        return False

    hashed_password = auth_dict.get(login)
    hashed_request_password = strategy(password)

    if hashed_password != hashed_request_password:
        return False

    return True


def basic_auth_middleware(
    urls: Iterable,
    auth_dict: dict,
    strategy: Type[BaseStrategy] = lambda x: x
) -> Coroutine:
    async def factory(app, handler) -> Coroutine:
        async def middleware(request) -> web.Response:
            for url in urls:
                if not request.path.startswith(url):
                    continue

                if inspect.isclass(strategy) and issubclass(strategy, BaseStrategy):
                    log.debug("Use Strategy: %r", strategy.__name__)
                    strategy_obj = strategy(
                        request,
                        auth_dict,
                        handler,
                        request.headers.get('Authorization', '')
                    )
                    return await strategy_obj.check()

                if not check_access(auth_dict, request.headers.get('Authorization', ''), strategy):
                    raise web.HTTPUnauthorized(headers={'WWW-Authenticate': 'Basic'})

                return await handler(request)
            return await handler(request)
        return middleware
    return factory
