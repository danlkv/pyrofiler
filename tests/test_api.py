import time
from pyrofiler import Profiler
import pyrofiler


def test_callback_default(capsys):
    # 1. Test printer enabled by default
    prof = Profiler()
    with prof.timing('test descr', foo=1):
        1+1
    cap = capsys.readouterr()
    assert 'test descr' in cap.out
    print('<capsys1>', cap.out, '</capsys1>')
    assert 'foo' in cap.out

    # 2. Test printer disabling
    pyrofiler.disable_printing()

    with prof.timing('test descr2', foo2=1):
        1+1

    cap = capsys.readouterr()
    print('<capsys2>', cap.out, '</capsys2>')
    assert 'test descr2' not in cap.out
    assert 'foo2' not in cap.out

    # 3. Test custom default callback
    def custom_cb(*args, **kwargs):
        print('custom1', *args)

    pyrofiler.set_default_callback(custom_cb)
    with prof.timing('test descr3', foo3=1):
        1+1

    cap = capsys.readouterr()
    print('<capsys3>', cap.out, '</capsys3>')
    assert 'test descr3' in cap.out
    assert 'custom1' in cap.out
    assert 'foo3' not in cap.out

    pyrofiler.enable_printing()


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


