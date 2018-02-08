#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    'requests==1.1.0',
]

test_requirements = [
    'nose',
]

setup(
    name='emma-python',
    version='0.1.0',
    description="Python library for working with Emma API",
    long_description=readme,
    author="Travis Hathaway",
    author_email='thathaway@myemma.com',
    url='https://github.com/myemma/EmmaPython',
    packages=find_packages(include=['emma']),
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='emma',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
