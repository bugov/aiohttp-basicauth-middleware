import os
from setuptools import setup

from aiohttp_basicauth_middleware import __version__

requires = ['http_basic_auth', 'aiohttp']


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()


setup(
    # Basic package information:
    name='aiohttp-basicauth-middleware',
    version=__version__,
    py_modules=('aiohttp_basicauth_middleware',),

    # Packaging options:
    zip_safe=False,
    include_package_data=True,
    packages=('aiohttp_basicauth_middleware',),

    classifiers=[
        'License :: Public Domain',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # Package dependencies:
    requires=requires,
    tests_require=requires + ["pytest"],
    setup_requires=requires + ["pytest-runner"],
    install_requires=requires,

    # Metadata for PyPI:
    author='Georgy Bazhukov',
    author_email='georgy.bazhukov@gmail.com',
    license='BSD',
    url='https://github.com/bugov/aiohttp-basicauth-middleware',
    keywords='aiohttp security basicauth http middleware',
    description='An incredibly simple HTTP basic auth implementation for Aiohttp.',
    long_description=read('README.md')
)
