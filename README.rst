=========
Pyrofiler
=========


.. image:: https://img.shields.io/pypi/v/pyrofiler.svg
        :target: https://pypi.python.org/pypi/pyrofiler

.. image:: https://img.shields.io/travis/DaniloZZZ/pyrofiler.svg
        :target: https://travis-ci.com/DaniloZZZ/pyrofiler

.. image:: https://readthedocs.org/projects/pyrofiler/badge/?version=latest
        :target: https://pyrofiler.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status



Toolset for granular memory and cpu live profiling


Quick start
-----------

Contextmanager that measures time of execution

.. code-block:: python

    # examples/simple_profile.py
    import pyrofiler
    import time

    with pyrofiler.timing('Time elapsed'):
        time.sleep(1)

.. code-block:: console

    $ python simple_profile.py
    Time elapsed : 1.001563310623169


Decorators for profiling functions

.. code-block:: python

    # examples/simple_profile_cpu.py
    import pyrofiler

    @pyrofiler.cpu_util(description='Cpu usage')
    @pyrofiler.timed('Time elapsed')
    def sum_series(x, N):
        return sum([x**i/i for i in range(1, N)])

    sum_series(.3, 1000_000)

.. code-block:: console

    $ python simple_profile_cpu.py
    Time elapsed : 0.13478374481201172
    Cpu usage : 29.4

Aggregate the results in common context:

.. code-block:: python

    # examples/profile_with_context.py
    from pyrofiler import Profiler
    import time

    prof = Profiler()

    with prof.timing('Time 1'):
        time.sleep(1)

    with prof.timing('Time 2'):
        time.sleep(1.5)

    print('Profiling data recorded:')
    print(prof.data)

.. code-block:: console

    $ python profile_with_context.py                                                    
    Time 1 : 1.0011215209960938
    Time 2 : 1.5020403861999512
    Profiling data recorded:
    {'Time 1': 1.0011215209960938, 'Time 2': 1.5020403861999512}

You can use other actions, for example appending results to some list in data.
Check the `documentation <https://pyrofiler.readthedocs.io/en/latest/usage.html>`_ for more use cases


Similar products
----------------

- Syrpy https://github.com/jeetsukumaran/Syrupy 
- Scalene https://github.com/emeryberger/scalene
- ... and lots of `others <https://github.com/matuskosut/python-perfres/>`_

Problems
--------
Either you have a cli tool that profiles memory and cpu, but **no code api for granular data** 

or you have stuff like decorators and **no memory profiling**

Having a live dashboard would help also, use https://github.com/libvis for that


Features
--------

* TODO

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
