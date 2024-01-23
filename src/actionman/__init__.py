"""ActionMan"""


import io as _io
import sys as _sys

from actionman import io, log, pprint, shell


_sys.stdout = _io.TextIOWrapper(_sys.stdout.buffer, encoding='utf-8')
