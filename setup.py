#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.md').read()
history = open('HISTORY.md').read().replace('.. :changelog:', '')

setup(
    name='dborutils',
    version='0.3.2',
    description='DBOR Utilities contains shared classes related to our Database of Record Project',
    long_description=readme + '\n\n' + history,
    author='Josvic Zammit',
    author_email='jvzammit@gmail.com',
    url='https://github.com/NoodleEducation/dborutils',
    packages=[
        'dborutils',
    ],
    package_dir={'dborutils': 'dborutils'},
    include_package_data=True,
    install_requires=[
        'MySQL-python==1.2.5',
        'pymongo==2.6.3',
    ],
    license="BSD",
    zip_safe=False,
    keywords='dborutils',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
    ],
    test_suite='tests',
)
