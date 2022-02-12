"""Main module."""
from pyrofiler import (
    timed
    , timing
    , cpu_util
    , mem_util
    , callbacks
)

class Profiler:
    def __init__(self, callback=None):
        self.data = {}
        if callback is None:
            self._callback = self._cb_default
        else:
            self._callback = callback

    def use_append(self):
        self._callback = self._cb_append

    def set_callback(self, callback):
        """
        Set the callback function that is called after each measurement

        Args:
            callback: a function
        """
        self._callback = callback

    def get_callback(self):
        """
        Get the callback function
        """
        return self._callback

    def timing(self, desc, *args, **kwargs):
        return timing(desc, callback=self._callback, *args, **kwargs)

    def timed(self, desc, *args, **kwargs):
        return timed(desc, callback=self._callback, *args, **kwargs)

    def cpu(self, desc, *args, **kwargs):
        return cpu_util(desc, *args, callback=self._callback, **kwargs)

    def mem(self, desc, *args, **kwargs):
        return mem_util(desc, *args, callback=self._callback, *kwargs)

    def _cb_default(self, result, label, **kwargs):
        callbacks.default(result, label, **kwargs)
        self.data[label] = result

    def _cb_append(self, result, label, **kwargs):
        callbacks.default(result, label, **kwargs)
        #
        x = self.data.get(label)
        if x is None:
            self.data[label] = []

        self.data[label].append(result)
