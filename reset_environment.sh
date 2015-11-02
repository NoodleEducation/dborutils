#!/bin/sh

# pip and virtualenv must be pre-installed by Anisble in the Docker
# container.

find . -name '*.pyc' -delete
rm -rf virtualenv/
virtualenv virtualenv
virtualenv/bin/pip install -r requirements.txt
