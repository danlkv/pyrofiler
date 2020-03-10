"""Main module."""
from pyrofiler.profilers import (
    timed
    , timing
    , cpu_util
    , mem_util
    , printer
)

class Profiler:
    def __init__(self):
        self.data = {}

    def use_append(self):
        self.cb = self._cb_append

    def timing(self, desc):
        return timing(desc, callback=self.cb)

    def timed(self, desc):
        return timed(desc, callback=self.cb)

    def cpu(self, desc):
        return cpu_util(callback=self.cb, description=desc)

    def mem(self, desc):
        return mem_util(callback=self.cb, description=desc)

    def cb(self, result, **kwargs):
        printer(result, **kwargs)
        descr = kwargs.get('description')
        self.data[descr] = result

    def _cb_append(self, result, **kwargs):
        printer(result, **kwargs)
        descr = kwargs.get('description')
        #
        x = self.data.get(descr)
        if x is None:
            self.data[descr] = []

        self.data[descr].append(result)
