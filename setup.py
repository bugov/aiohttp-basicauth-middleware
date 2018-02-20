from os.path import abspath, dirname, join, normpath

from setuptools import setup

requires = ['basicauth', 'aiohttp']

setup(
    # Basic package information:
    name='aiohttp-basicauth-middleware',
    version='0.1.0',
    py_modules=('aiohttp_basicauth_middleware',),

    # Packaging options:
    zip_safe=False,
    include_package_data=True,

    classifiers=[
        'License :: Public Domain',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    # Package dependencies:
    test_suite="tests",
    requires=requires,
    tests_require=requires,
    setup_requires=requires,
    install_requires=requires,

    # Metadata for PyPI:
    author='Georgy Bazhukov',
    author_email='georgy.bazhukov@gmail.com',
    license='BSD',
    url='https://github.com/bugov/aiohttp-basicauth-middleware',
    keywords='aiohttp security basicauth http middleware',
    description='An incredibly simple HTTP basic auth implementation for Aiohttp.',
    long_description=open(
        normpath(join(dirname(abspath(__file__)), 'README.md')), encoding='utf-8'
    ).read()
)
