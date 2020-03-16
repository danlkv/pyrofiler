=====
Usage
=====

To use Pyrofiler in a project::

    import pyrofiler


All pyrofiler's tools work in a same fashion: after calling the function (or code if it's a contextmanager) 
and measuring data, a `callback` object is called.

Here's a default callback that prints the data:

.. code-block:: python 

    def printer(result, description='Profile results'):
        print(description, ':', result)

Any arguments to a tool expect the `callback` argument are passed
to the callback function.

Here's how the callback is called:

.. code-block:: python 

    callback(profiling_result, *args, **kwargs)

Where `args` and `kwargs` are arguments to the tool.

For example, this is the code for timing tool:


.. code-block:: python 

    def timing(*args, callback=printer, **kwargs) -> None:
        start = time()
        yield
        ellapsed_time = time() - start
        callback(ellapsed_time, *args, **kwargs)

