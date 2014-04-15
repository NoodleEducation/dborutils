from datetime import datetime
from sys import stderr, stdout
from traceback import extract_stack


class NoodleLogger(object):

    def logger(self, lvl, msg):

        (
            procName,
            lineNum,
            funcName,
            _,
        ) = extract_stack()[len(extract_stack()) - 2]

        msg = "{0} {1} {5}\n".format(
            datetime.now(),
            lvl,
            procName,
            funcName,
            lineNum,
            msg,
        )

        ioStream = dict(error=stderr).get(lvl, stdout)
        print >> ioStream, msg,
        ioStream.flush()

