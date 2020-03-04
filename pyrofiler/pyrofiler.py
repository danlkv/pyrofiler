"""Main module."""
from pyrofiler.profilers import (
    timed
    , cpu_util
    , mem_util
)

class Profiler:
    def __init__(self):
        self.data = {}

    def timing(self, description):
        return timed(description)

    def cpu(self, description):
        return cpu_util(description=description)

    def mem(self, description):
        return mem_util(description=description)
