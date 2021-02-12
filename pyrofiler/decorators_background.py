from functools import wraps
import time

import pyrofiler
import psutil, os


def measure2decor(measure):
    def _wrapper(*m_args, **m_kwargs):
        # Measure will get *args, **kwargs from this call
        def _decorator(profilee):
            @wraps(profilee)
            def wrap(*args, **kwargs):
                killpill = pyrofiler.threading.start_in_thread(measure, *m_args, **m_kwargs)
                try:
                    ret = profilee(*args, **kwargs)
                except BaseException as e:
                    killpill.stop()
                    raise
                killpill.stop()
                res = killpill.get_result()
                if isinstance(res, Exception):
                    print('Exception while profiling:', res)
                return ret
            return wrap
        return _decorator
    return _wrapper


proc_count = measure2decor(pyrofiler.measures.proc_count)
cpu_util = measure2decor(pyrofiler.measures.cpu_util)
mem_util = measure2decor(pyrofiler.measures.mem_util)
