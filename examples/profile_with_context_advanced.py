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
        data = self.data[label]
        return dict(
            mean=np.mean(data),
            max = np.max(data),
            std = np.std(data),
            min = np.min(data)
        )

prof = MyProfiler()
pyrofiler.PROF = prof

def my_function(i):
    with prof.timing('My_func_time'):
        time.sleep(i)

def main():
    with prof.timing('Main'):
        for i in range(10):
            my_function(i/20)
        another_file.func1()

main()
print('Pyrofiler data', prof.data)
print('Pyrofiler main', prof.data['Main'])
print('Pyrofiler my_function sum', sum(prof.data['My_func_time']))
print('Overhead of python/pyrofiler', prof.data['Main'][0] - sum(prof.data['My_func_time']))
print('Stats', prof.get_stats('My_func_time'))
