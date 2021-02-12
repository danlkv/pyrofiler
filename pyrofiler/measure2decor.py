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


def start_in_thread(f, *args, **kwargs):
    """
    Start a function in thread.

    The first argument of function will be generator,
    which stops when function is asked to exit

    Args:
        f (callable): function that accepts
             a generator as first argument and
             returns shortly after generotor stops

    Returns:
        killpill: object with .stop() method which stops the
            generator
    """
    gen = WatchdogGen()
    func = pyrofiler.threaded_with_queue(f)
    thread, queue = func(gen, *args, **kwargs)

    def _onstop():
        gen.stop()
        thread.join()

    pill = KillPill(on_stop=_onstop, get_result=queue.get)
    #st = time.time() #--
    while True:
        if gen.started:
            break
        else:
            #print('wait for start')
            # A very small number is enough, since 
            # we just need to trigger a thread switch
            time.sleep(0.0002)
    #print('overhead thread start', time.time()-st) #--

    return pill


def measure2decor(measure):
    def _wrapper(*m_args, **m_kwargs):
        # Measure will get *args, **kwargs from this call
        def _decorator(profilee):
            @wraps(profilee)
            def wrap(*args, **kwargs):
                killpill = start_in_thread(measure, *m_args, **m_kwargs)
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
