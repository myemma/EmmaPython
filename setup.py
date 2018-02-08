#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

try:
   import pypandoc
   readme = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
   readme = ''

requirements = [
    'requests==1.1.0',
]

test_requirements = [
    'nose',
]

setup(
    name='emma-python',
    version='1.0.0',
    description="Python library for working with Emma API",
    long_description=readme,
    author="Doug Hurst",
    author_email='support@myemma.com',
    url='https://github.com/myemma/EmmaPython',
    packages=find_packages(include=[
        'emma',
        'emma.adapter',
        'emma.model',
        'emma.query'
    ]),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='emma',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'License :: OSI Approved :: MIT License',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    license='MIT'
)
