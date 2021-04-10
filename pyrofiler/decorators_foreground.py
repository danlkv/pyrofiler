from time import time, sleep
from contextlib import contextmanager
import pyrofiler
from functools import wraps
import psutil
import os
from pyrofiler.threading import threaded_gen
import pyrofiler.callbacks as callbacks


def profile_decorator(profiler):
    """ Factory of profilling decorator functions

        Takes a function `profiler` and returns a decorator,
        which takes a function to profile, `profilee`,
        starts it in separate thread and
        passes `profiler` a generator that iterates
        while the therad with `profilee` is running.
        Last vaulue of the generator will be a return value of `profilee`

        Usage:
            @profile_decorator
            def cpu_load(gen, output_fmt='cpu_vals='):
                cpus = []
                while ret in gen:
                    cpus.append(get_cpu_util())
                print(output_fmt, cpus)
                return ret

        Returns:
            profiler_kwargs -> decorator -> wrapped_callable
    """

    def _wrapper(*profiler_args, **profiler_kw):
        def _decorator(profilee):
            """Call profilee in a thread, while running profiler."""
            @wraps(profilee)
            def wrap(*args, **kwargs):
                thr_gen = threaded_gen(profilee)
                gen = thr_gen(*args, **kwargs)
                res = profiler(gen, *profiler_args, **profiler_kw)
                return res
            return wrap
        return _decorator
    return _wrapper


def timed(*args, callback=callbacks.default, **kwargs):
    def decor(func):
        @wraps(func)
        def wrapped(*a,**kw):
            start = time()
            x = func(*a, **kw)
            ellapsed_time = time() - start
            callback(ellapsed_time, *args, **kwargs)
            return x
        return wrapped
    return decor


proc_count = profile_decorator(pyrofiler.measures.proc_count)
cpu_util = profile_decorator(pyrofiler.measures.cpu_util)
mem_util = profile_decorator(pyrofiler.measures.mem_util)
