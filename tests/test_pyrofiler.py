#!/usr/bin/env python

"""Tests for `pyrofiler` package."""
import sys
from math import sin, cos, radians
import time

from pyrofiler.pyrofiler import Profiler


def test_time(capsys):
    descr = 'test descr'
    sleep_time = .3
    p = Profiler()

    # -- actual test
    @p.timing(descr)
    def sleep_x(x):
        time.sleep(x)
    sleep_x(sleep_time)
    # --

    out, err = capsys.readouterr()
    assert descr in out
    # Last number is the value
    assert abs(sleep_time - float(out.split()[-1])) <.001

def test_cpu(capsys):
    descr = 'test descr cpu'
    p = Profiler()

    # -- actual test
    @p.timing(descr)
    def bench():
        """ Multiplies 1 by sin^2 + cos^2 for all angles """
        product = 1.0
        for counter in range(1, 1000, 1):
            for dex in list(range(1, 360, 1)):
                angle = radians(dex)
                product *= sin(angle)**2 + cos(angle)**2
        return product
    x = bench()
    assert abs(x-1)<.0001
    # --

    out, err = capsys.readouterr()
    assert descr in out
    # Last number is the value
    assert float(out.split()[-1]) > .001

