#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    'Flask',
    'PyExifTool',
    'SQLAlchemy',
    'arrow',
    'python-magic',
    'pyxdg',
    'voluptuous',
]

test_requirements = [
    'coverage',
    'pillow',
]

setup(
    name='pic2map',
    version='0.1.0',
    description="Display pictures location in a map",
    long_description=readme + '\n\n' + history,
    author="Javier Collado",
    author_email='jcollado@nowsecure.com',
    url='https://github.com/jcollado/pic2map',
    packages=[
        'pic2map',
    ],
    package_dir={'pic2map': 'pic2map'},
    package_data={'pic2map': [
        'server/templates/*.html',
        'server/static/*.css',
        'server/static/*.js',
    ]},
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='picture map location',
    entry_points={
        'console_scripts': [
            'pic2map = pic2map.cli:main',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
