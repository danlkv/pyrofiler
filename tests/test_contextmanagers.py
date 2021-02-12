import numpy as np
from math import sin, cos, radians
import time
import sys
import pyrofiler
import pyrofiler.c as prof


def sizeof(obj):
    size = sys.getsizeof(obj)
    if isinstance(obj, dict): return size + sum(map(sizeof, obj.keys())) + sum(map(sizeof, obj.values()))
    if isinstance(obj, (list, tuple, set, frozenset)): return size + sum(map(sizeof, obj))
    return size


def test_time():
    with prof.timing() as time_prof:
        time.sleep(0.3)

    measure = time_prof.result
    assert np.isclose(
        measure, 0.3, rtol=5e-3)


def test_mem():
    consume_bytes = 10*1000*1000 # 10MB

    with prof.mem_util() as mem_prof:
        consume_memory = list(range(consume_bytes//(28+8)))
        print('better sizeof', sizeof(consume_memory))
        # wait so profiler catches the stuff
        time.sleep(0.3)

    measure = mem_prof.result
    print('Memory measure', measure)
    assert np.isclose(
        measure, consume_bytes+1000_000, rtol=9e-2)


def test_cpu(capsys):
    descr = 'test descr cpu'

    # -- actual test
    with prof.cpu_util(descr) as cpu_prof:
        product = 1.0
        for counter in range(1, 1000, 1):
            for dex in list(range(1, 360, 1)):
                angle = radians(dex)
                product *= sin(angle)**2 + cos(angle)**2
    # Last number is the value
    assert cpu_prof.get_result() > .001
