aiohttp-basicauth-middleware
============================

.. figure:: https://travis-ci.org/bugov/aiohttp-basicauth-middleware.svg?branch=master


Aiohttp middleware for simple http basic
auth protection for some urls.

Works with Python >= 3.5.

Works with UTF-8 🖖

Installation
------------

.. code:: bash

    pip install aiohttp-basicauth-middleware

Usage
-----

.. code:: python

    app = web.Application(loop=loop)
    
    app.router.add_route('GET', '/hello', handler_a)
    app.router.add_route('GET', '/admin/hello', handler_b)

    app.middlewares.append(
        basic_auth_middleware(
            ('/admin',),
            {'user': 'password'},
        )
    )


`basic_auth_middleware` has 3 params:

1. list of protected urls. For example `['/admin']` will match
   with `/admin/user`, but will not match with `/user/admin`.
2. auth dict – a dict with pairs: login-password.
3. strategy (optional) for password comparision. For example you can
   store hashed password in `auth_dict`. See `aiohttp_basicauth_middleware.strategy.BaseStrategy` and
   `example.strategy` for more information.

Example with md5 password hashing:

.. code:: python

    app = web.Application(loop=loop)

    app.router.add_route('GET', '/hello', handler_a)
    app.router.add_route('GET', '/admin/hello', handler_b)

    app.middlewares.append(
        basic_auth_middleware(
            ('/admin',),
            {'user': '5f4dcc3b5aa765d61d8327deb882cf99'},
            lambda x: hashlib.md5(bytes(x, encoding='utf-8')).hexdigest(),
        )
    )

`/admin/...` will be accessed by the same login+password pair ('user', 'password').
