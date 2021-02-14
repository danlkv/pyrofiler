"""Top-level package for Pyrofiler."""

__author__ = """Dan Lykov"""
__email__ = 'lkv97dn@gmail.com'
__version__ = '0.1.5'

import sys

from . import callbacks
from .callbacks import printer
from pyrofiler.threading import threaded, threaded_with_queue
from pyrofiler import measures
from pyrofiler.decorators_foreground import (
    timed
)
from pyrofiler.decorators_background import measure2decor
from pyrofiler.d import (
     cpu_util, mem_util, proc_count,
)

from pyrofiler.contextmanagers import (
     timing
)

from pyrofiler.pyrofiler import Profiler
