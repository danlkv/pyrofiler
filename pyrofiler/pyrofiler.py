"""Main module."""
from pyrofiler.profilers import (
    timed
    , cpu_util
    , mem_util
)

class Profiler:
    def __init__(self):
        self.data = {}

    def timing(self, desc):
        return timed(desc)

    def cpu(self, desc):
        return cpu_util(description=desc)

    def mem(self, desc):
        return mem_util(description=desc)

    def cb(self, result, **kwargs):
        print('profiler!,', result)
