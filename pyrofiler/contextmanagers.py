import pyrofiler
from functools import lru_cache
from pyrofiler import measure2decor
from pyrofiler.threading import KillPill
from contextlib import contextmanager
import time
import queue


def printer(result, description='Profile results'):
    print(description, ':', result)


def measure2context(measure):
    @contextmanager
    def measuring_manager(*m_args, **m_kwargs):
        # -- Getting result from measure
        q = queue.Queue()
        clb = m_kwargs.pop('callback', None)
        def callback(res, *args, **kwargs):
            if clb:
                clb(res, *args, **kwargs)
            q.put(res)
        m_kwargs['callback'] = callback
        # --

        killpill = pyrofiler.threading.start_in_thread(
            measure, *m_args, **m_kwargs)
        killpill.get_result = lru_cache(q.get)
        try:
            yield killpill
        except BaseException:
            killpill.stop()
            raise
        killpill.stop()
        res = killpill.get_result()
        if isinstance(res, Exception):
            print('Exception while profiling:', res)
    return measuring_manager


@contextmanager
def timing(*args, callback=printer, **kwargs) -> None:
    start = time.time()
    q = queue.Queue()
    yield KillPill(
        on_stop=lambda:None,
        get_result=lru_cache(q.get)
    )
    ellapsed_time = time.time() - start
    q.put(ellapsed_time)
    callback(ellapsed_time, *args, **kwargs)


proc_count = measure2context(pyrofiler.measures.proc_count)
cpu_util = measure2context(pyrofiler.measures.cpu_util)
mem_util = measure2context(pyrofiler.measures.mem_util)
