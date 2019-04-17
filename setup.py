#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


def fread(filepath, skip_lines=0):
    with open(filepath, 'r') as f:
        return ''.join(f.readlines()[skip_lines:])


setup(
    name='GB2260-v2',
    version='0.2.0',
    url='https://github.com/bosndata/GB2260.py',
    packages=find_packages(exclude=('tests', 'tests.*')),
    description='The Python implementation for looking up the Chinese '
                'administrative divisions.',
    long_description=fread('README.rst', skip_lines=2),
    license='BSD',
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: Chinese (Simplified)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ]
)
