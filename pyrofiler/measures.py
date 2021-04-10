import psutil
import os

import pyrofiler.callbacks as callbacks


def proc_count(gen, *args, callback=callbacks.default, **kwargs):
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


def mem_util(gen, *args, subtract_overhead=True, callback=callbacks.default, **kwargs):
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


def cpu_util(gen, *args, callback=callbacks.default, **kwargs):
    utils = []
    res = None
    for res in gen:
        utils.append(psutil.cpu_percent(interval=0))
    profiling_result = max(utils)
    callback(profiling_result, *args, **kwargs)
    return res
