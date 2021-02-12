from functools import wraps
import time

import pyrofiler
import psutil, os


class KillPill:
    def __init__(self, on_stop, get_result):
        self.on_stop = on_stop
        self.get_result = get_result

    def stop(self):
        self.on_stop()

    @property
    def result(self):
        return self.get_result()

class WatchdogGen:
    """
    An indefinitely-running generator
    with a stop() method
    """
    def __init__(self):
        self.running = True
        self.started = False

    def __iter__(self):
        self.started = True
        while True:
            if self.running:
                yield
                time.sleep(.1)
            else:
                break

    def stop(self):
        self.running = False


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
