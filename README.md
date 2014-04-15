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

### MySQL-related OS X specific warnings

During installation some warnings may be generated on OS X computers by the installation of `MySQL-python` package.

Sample output:

```
Running MySQL-python-1.2.5/setup.py -q bdist_egg --dist-dir /var/folders/j3/3ynw0g6s26v6bl7l3gfyv93c0000gn/T/easy_install-DcLALC/MySQL-python-1.2.5/egg-dist-tmp-ZDB0K5
In file included from _mysql.c:44:
/usr/local/mysql/include/my_config.h:348:11: warning: 'SIZEOF_SIZE_T' macro redefined
  #define SIZEOF_SIZE_T  SIZEOF_LONG
          ^
/usr/local/Cellar/python/2.7.6/Frameworks/Python.framework/Versions/2.7/include/python2.7/pymacconfig.h:43:17: note:
      previous definition is here
#        define SIZEOF_SIZE_T           8
                ^
In file included from _mysql.c:44:
/usr/local/mysql/include/my_config.h:442:9: warning: 'HAVE_WCSCOLL' macro redefined
#define HAVE_WCSCOLL
        ^
/usr/local/Cellar/python/2.7.6/Frameworks/Python.framework/Versions/2.7/include/python2.7/pyconfig.h:908:9: note:
      previous definition is here
#define HAVE_WCSCOLL 1
        ^
_mysql.c:1589:10: warning: comparison of unsigned expression < 0 is always false
      [-Wtautological-compare]
        if (how < 0 || how >= sizeof(row_converters)) {
            ~~~ ^ ~
3 warnings generated.
zip_safe flag not set; analyzing archive contents...
Adding MySQL-python 1.2.5 to easy-install.pth file

Installed /Users/josvic/venvs/dbuenv/lib/python2.7/site-packages/MySQL_python-1.2.5-py2.7-macosx-10.9-x86_64.egg
Finished processing dependencies for dborutils==0.1.0
```

If you have `MySQL-python` already installed, use:

```
ARCHFLAGS="-arch $(uname -m)" pip install mysql-python
```
\
as suggested by this [answer on SO](http://stackoverflow.com/a/6853460/1211429). Note that you don't need to `sudo` as long as you're installing `MySQL-python` in a virtualenv.

## Usage

You can import, for instance, the `NoodleLogger` class, this way:

```
from dborutils.logger import NoodleLogger
```
