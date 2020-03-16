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
        return cpu_util(desc, callback=self.cb)

    def mem(self, desc):
        return mem_util(desc, callback=self.cb)

    def cb(self, result, label, **kwargs):
        printer(result, label, **kwargs)
        self.data[label] = result

    def _cb_append(self, result, label, **kwargs):
        printer(result, label, **kwargs)
        #
        x = self.data.get(label)
        if x is None:
            self.data[label] = []

        self.data[label].append(result)
