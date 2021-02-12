#!/usr/bin/env python

"""Tests for `pyrofiler` package."""
import sys
import numpy as np
from math import sin, cos, radians
import time
import pytest

from pyrofiler.pyrofiler import Profiler


def sizeof(obj):
    size = sys.getsizeof(obj)
    if isinstance(obj, dict): return size + sum(map(sizeof, obj.keys())) + sum(map(sizeof, obj.values()))
    if isinstance(obj, (list, tuple, set, frozenset)): return size + sum(map(sizeof, obj))
    return size


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
    @p.cpu(descr)
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
    print(out)
    # Last number is the value
    assert float(out.split()[-1]) > .001


def test_mem(capsys):
    descr = 'test descr mem'
    consume = 10*1000*1000 # 10MB
    p = Profiler()

    # -- actual test
    @p.mem(descr)
    def bench(consume_bytes):
        # sys.getsizeof may not be what I want
        # https://nedbatchelder.com/blog/202002/sysgetsizeof_is_not_what_you_want.html
        # list datastructure costs 8 bytes per item
        # integer costs 28 bytes
        consume_memory = list(range(consume_bytes//(28+8)))
        #print(sys.getsizeof(consume_memory))
        print('better sizeof', sizeof(consume_memory))
        # wait so profiler catches the stuff
        time.sleep(0.3)
    x = bench(consume)
    # --

    out, err = capsys.readouterr()
    print(out)
    assert descr in p.data.keys()
    # Last number is the value
    # pure Python has about 24MB overhead
    # results in 5x size of actual valriable (75M - 24M). Why? (numpy does not do this)
    measure = p.data[descr]
    print('Memory measure', measure)
    assert np.isclose(measure, consume, rtol=2e-1)

def test_mem_np(capsys):
    descr = 'test descr mem'
    consume = 10*1000*1000 # 10MB
    p = Profiler()

    # -- actual test
    @p.mem(descr)
    def bench(consume_bytes):
        # which to use for np: rss or virt? https://github.com/dask/distributed/issues/1409

        # ones take less memory in fact
        consume_memory = np.ones(consume_bytes//8)
        print(sys.getsizeof(consume_memory))
        # wait so profiler catches the stuff
        time.sleep(0.3)
    x = bench(consume)
    # --

    out, err = capsys.readouterr()
    print(out)
    assert descr in p.data.keys()
    # Last number is the value
    # For some reason, the actual memory usage is smaller than
    # expected 10M
    measure = p.data[descr]
    print('Memory measure', measure)
    assert np.isclose(measure, consume, rtol=3e-2)
