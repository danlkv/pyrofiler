from threading import Thread
import queue
from time import sleep
import time
from functools import lru_cache


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
            for _ in range(20):
                if self.running:
                    sleep(.0005)
                else:
                    return

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
    func = threaded_with_queue(f)
    thread, queue = func(gen, *args, **kwargs)

    def _onstop():
        gen.stop()
        #thread.join()

    pill = KillPill(
        on_stop=_onstop,
        # The result is retreived once, but can be requested
        # multiple times. Will break if measure returns
        # numpy arrays, however.
        get_result=lru_cache(queue.get)
    )
    #st = time.time() #--
    while True:
        if gen.started:
            break
        else:
            #print('wait for start')
            # A very small number is enough, since 
            # we just need to trigger a thread switch
            sleep(0.00002)
    #print('overhead thread start', time.time()-st) #--

    return pill

def threaded(daemon=False):
    """Start a function in a thread.
        Returns:
            threading.Thread: thread object with function
    """
    def _decorator(func):
        def _wrapped(*args, **kwargs):
            t = Thread(target=func, args=args, kwargs=kwargs)
            t.daemon = daemon
            t.start()
            return t
        return _wrapped
    return _decorator

def threaded_with_queue(func, daemon=False):
    """Start a function in a thread, return result queue

    Args:
        func (function): function to call
        daemon (bool): whether the thread should be daemon

    Returns:
        function: function that starts a thread with `func`
            and returns tuple (threading.Thread, queue.Queue)
    """

    def wrapped_f(q, *args, **kwargs):
        """"Call `func` and put result result in the queue."""
        try:
            ret = func(*args, **kwargs)
            q.put(ret)
        except Exception as e:
            q.put(e)


    def _wrapped(*args, **kwargs):
        q = queue.Queue()
        t = Thread(target=wrapped_f, args=(q,)+args, kwargs=kwargs)
        t.daemon = daemon
        # takes ~4 ms
        t.start()
        return t, q

    return _wrapped

def threaded_gen(f):
    """ makes the function return a generator, 
    which iterates while thread is running and 
    yields return value of function at last step.
    Usage:
        for res it threaded_gen(f)(*args, **kw):
            #do stuff here
        print('Done threaded exec:',res)
    """

    def wrap(*args, **kwargs):
        thr_f = threaded_with_queue(f)
        thread, result_queue = thr_f(*args, **kwargs)
        while thread.is_alive():
            yield
            # TODO: would be nice to set up the timedelta
            sleep(.1)
        thread.join()
        res = result_queue.get()
        if isinstance(res, Exception):
            raise res
        yield res
        return
    return wrap

