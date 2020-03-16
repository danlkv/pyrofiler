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

Any arguments to a tool expect the `callback` argument are passed as 
keyword arguments to the callback function.

.. code-block:: python 

    callback(profiling_result, **kwargs)
