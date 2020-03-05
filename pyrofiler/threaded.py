from threading import Thread
import queue
from time import sleep

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
        ret = func(*args, **kwargs)
        q.put(ret)

    def _wrapped(*args, **kwargs):
        q = queue.Queue()
        t = Thread(target=wrapped_f, args=(q,)+args, kwargs=kwargs)
        t.daemon = daemon
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
        yield result_queue.get()
        return
    return wrap

