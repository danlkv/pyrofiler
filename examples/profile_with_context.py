from pyrofiler import Profiler
import time

prof = Profiler()

with prof.timing('Time 1'):
    time.sleep(1)

with prof.timing('Time 2'):
    time.sleep(1.5)

print('Profiling data recorded:')
print(prof.data)
