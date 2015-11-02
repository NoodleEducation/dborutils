#!/bin/bash

set -e

virtualenv/bin/flake8 dborutils tests
virtualenv/bin/nosetests `find tests -type f | grep 'test_.*\.py$'`


