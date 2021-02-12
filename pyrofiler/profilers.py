from time import time, sleep
from contextlib import contextmanager
from functools import wraps
import psutil
import os
from pyrofiler.threaded import threaded_gen

def printer(result, description='Profile results'):
    print(description, ':', result)


@contextmanager
def timing(*args, callback=printer, **kwargs) -> None:
    start = time()
    yield
    ellapsed_time = time() - start
    callback(ellapsed_time, *args, **kwargs)

def timed(*args, callback=printer, **kwargs):
    def decor(func):
        @wraps(func)
        def wrapped(*a,**kw):
            with timing(*args, callback=callback, **kwargs):
                x = func(*a, **kw)
            return x
        return wrapped
    return decor


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

@profile_decorator
def proc_count(gen, *args, callback=printer, **kwargs):
    pnames = set()
    res = None
    for res in gen:
        names = [proc.name() for proc in psutil.process_iter()]
        names = {name + str(i) for i, name in enumerate(names) 
                 if 'python' in name}
        pnames = pnames | names
    profiling_result = len(pnames)
    callback(profiling_result, *args, **kwargs)
    return res

@profile_decorator
def cpu_util(gen, *args, callback=printer, **kwargs):
    utils = []
    res = None
    for res in gen:
        utils.append(psutil.cpu_percent(interval=0))
    profiling_result = max(utils)
    callback(profiling_result, *args, **kwargs)
    return res

@profile_decorator
def mem_util(gen, *args, subtract_overhead=True, callback=printer, **kwargs):
    utils = []
    res = None
    process = psutil.Process(os.getpid())
    overhead = process.memory_info().rss
    for res in gen:
        #https://psutil.readthedocs.io/en/latest/index.html#psutil.Process.memory_info
        mem_info = process.memory_info()
        #print(mem_info)
        utils.append(mem_info.rss)
    profiling_result = max(utils)
    if subtract_overhead:
        profiling_result -= overhead
    callback(profiling_result, *args, **kwargs)
    return res

