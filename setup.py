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

setup(
    name='dborutils',
    version='0.4.4',
    description='DBOR Utilities contains code shared between multiple Noodle repositories.',
    long_description=readme,
    author='Noodle',
    author_email='data@noodle.com',
    url='https://github.com/NoodleEducation/dborutils',
    packages=[
        'dborutils',
    ],
    package_dir={'dborutils': 'dborutils'},
    include_package_data=True,
    install_requires=[
        'pymongo==2.7.1',
        'wheel=0.23.0',
        'numpy==1.9',
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
