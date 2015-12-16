# dborutils

Shared classes related to our Database of Record Project

## Installation

Execute:

```
pip install git+https://github.com/NoodleEducation/dborutils
```

To install a particular branch only:

```
pip install git+https://github.com/NoodleEducation/dborutils.git@[branch-name]
```
### Github Two Factor Authentication

If you have enabled Github two factor authentication, then you will need to provide
an auth token instead of your password when installing. You create and save a token
on Github's site.

## Running Tests
To run the tests, you will need to create a virtualenv first:
1. Install virtualenv
```
pip install virtualenv
```

2. Create a virtualenv in dborutils
```
cd /path/to/dborutils/ && virtualenv virtualenv
```

3. Install requirements
```
virtualenv/bin/pip install -r requirements.txt
```

4. Run tests
```
make test
```

## Usage

You can import, for instance, the `MongoCollection` class, this way:

```
from dborutils.mongo import MongoCollection
```
