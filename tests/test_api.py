from pyrofiler import Profiler

def test_callback_api():
    def callback(time, descr, foo=None):
        assert foo is 1
        assert descr is 'test descr'
        assert type(time) is float
    prof = Profiler(callback=callback)
    with prof.timing('test descr', foo=1):
        1+1



