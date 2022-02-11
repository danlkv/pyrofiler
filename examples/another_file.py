import pyrofiler
import time

def func1():
    # use PROF defined in profile_with_context_advanced.py
    with pyrofiler.PROF.timing('from another file'):
        time.sleep(.155)
    return 1


