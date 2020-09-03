import pytest
from pyrofiler.pyrofiler import Profiler
from pyrofiler import timed, cpu_util


@timed('Some strange function')
def raises_t():
    raise Exception('oops time')

@cpu_util('Some strange function')
def raises_cpu():
    raise Exception('oops cpu')


def test_raises_func():
    with pytest.raises(Exception):
        raises_cpu()

    with pytest.raises(Exception) as ex:
        raises_t()
    assert str(ex.value) == 'oops time'

def test_raises_prof():
    prof = Profiler()
    with pytest.raises(Exception) as ex:
        with prof.timing('Test raises'):
            raise Exception('whoops')
    assert str(ex.value) == 'whoops'
