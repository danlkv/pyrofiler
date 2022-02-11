from pyrofiler import Profiler
import pyrofiler
import another_file
import numpy as np
import time

class MyProfiler(Profiler):
    def __init__(self, callback=None):
        super().__init__(callback=callback)
        self.use_append()

    def get_stats(self, label):
        data = [x['value'] for x in self.data[label]]
        return dict(
            mean=np.mean(data),
            max = np.max(data),
            std = np.std(data),
            min = np.min(data)
        )

prof = MyProfiler()
pyrofiler.PROF = prof
default_cb = prof._callback
def my_callback(value, desc, reference=0):
    default_cb(dict(reference=reference, value=value), desc)
    
prof._callback = my_callback

def my_function(i):
    with prof.timing('My_func_time', reference=i):
        time.sleep(i)

def main():
    with prof.timing('Main'):
        for i in range(10):
            my_function(i/20)
        another_file.func1()

main()
print('Pyrofiler data', prof.data)
print('Pyrofiler main', prof.data['Main'])
print('Stats', prof.get_stats('My_func_time'))
