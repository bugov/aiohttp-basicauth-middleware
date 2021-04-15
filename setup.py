import os
from setuptools import setup


requires = ['wheel', 'http_basic_auth', 'aiohttp']


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding='utf-8').read()


setup(
    # Basic package information:
    name='aiohttp-basicauth-middleware',
    version='1.1.3',
    py_modules=('aiohttp_basicauth_middleware',),

    # Packaging options:
    zip_safe=False,
    include_package_data=True,
    packages=('aiohttp_basicauth_middleware',),

    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
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
    long_description=read('README.rst')
)
