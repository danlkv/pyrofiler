from threading import Thread
import queue
from time import sleep

def threaded(daemon=False):
    """
    Return a function that starts in thread and returns the thead object
    """
    def _decorator(func):
        def _wrapped(*args, **kwargs):
            t = Thread(target=func, args=args, kwargs=kwargs)
            t.daemon = daemon
            t.start()
            return t
        return _wrapped
    return _decorator

def threaded_with_queue(f, daemon=False):
    def wrapped_f(q, *args, **kwargs):
        '''this function calls the decorated function and puts the 
        result in a queue'''
        ret = f(*args, **kwargs)
        q.put(ret)

    def wrap(*args, **kwargs):
        '''this is the function returned from the decorator. It fires off
        wrapped_f in a new thread and returns the thread object with
        the result queue attached'''

        q = queue.Queue()
        t = Thread(target=wrapped_f, args=(q,)+args, kwargs=kwargs)
        t.daemon = daemon
        t.start()
        t.result_queue = q
        return t

    return wrap

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
        thr_f =  threaded_with_queue(f)
        thread = thr_f(*args, **kwargs)
        while thread.is_alive():
            yield
            # TODO: would be nice to set up the timedelta
            sleep(.1)
        thread.join()
        yield thread.result_queue.get()
        return
    return wrap

