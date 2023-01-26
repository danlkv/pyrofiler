import pyrofiler
from functools import lru_cache
from pyrofiler import measure2decor
from pyrofiler.threading import KillPill
from contextlib import contextmanager
import time
import queue
import pyrofiler.callbacks as callbacks


def measure2context(measure):
    @contextmanager
    def measuring_manager(*m_args, **m_kwargs):
        # -- Getting result from measure
        #st = time.time()
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
        #print('starting overhead', time.time()-st)
        try:
            yield killpill
        except BaseException:
            killpill.stop()
            raise
        #st = time.time()
        killpill.stop()
        #print('stopping', time.time()-st)
        #st = time.time()
        res = killpill.get_result()
        #print('getting', time.time()-st)
        if isinstance(res, Exception):
            print('Exception while profiling:', res)
    return measuring_manager


@contextmanager
def timing(*args, callback=callbacks.default, **kwargs) -> None:
    q = queue.Queue()
    kp = KillPill(
        on_stop=lambda:None,
        get_result=lru_cache(q.get)
    )
    start = time.time()
    yield kp
    ellapsed_time = time.time() - start
    q.put(ellapsed_time)
    callback(ellapsed_time, *args, **kwargs)

@contextmanager
def timing_gpu(*args, callback=callbacks.default, **kwargs) -> None:
    import torch
    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)
    q = queue.Queue()
    kp = KillPill(
        on_stop=lambda:None,
        get_result=lru_cache(q.get)
    )
    start.record()
    yield kp
    end.record()
    torch.cuda.synchronize()
    ellapsed_time = start.elapsed_time(end)/1000
    q.put(ellapsed_time)
    callback(ellapsed_time, *args, **kwargs)


proc_count = measure2context(pyrofiler.measures.proc_count)
cpu_util = measure2context(pyrofiler.measures.cpu_util)
mem_util = measure2context(pyrofiler.measures.mem_util)
