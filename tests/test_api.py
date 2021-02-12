import time
from pyrofiler import Profiler
import pyrofiler

def test_callback_api():
    def callback(time, descr, foo=None):
        assert foo is 1
        assert descr is 'test descr'
        assert type(time) is float
    prof = Profiler(callback=callback)
    with prof.timing('test descr', foo=1):
        1+1

    def print_spicy_time(time, spice):
        print(f'Spice {spice} took {time} seconds')

    @pyrofiler.timed(spice='spicy', callback=print_spicy_time)
    def spicy_sleep():
        time.sleep(.1)

    spicy_sleep()

    with pyrofiler.timing(spice='spicy', callback=print_spicy_time):
        time.sleep(.1)


