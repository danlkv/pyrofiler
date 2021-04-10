def nothing(*args, **kwargs):
    pass

def printer(result, description='Profile results', **kwargs):
    if kwargs:
        details = ' ' + str(kwargs)
    else:
        details = ''
    print(description+details, ':', result)

_DEFAULT_CLB = printer

def default(*args, **kwargs):
    """ Default callback, can be set
    using :meth:`pyrofiler.set_default_callback`

    Internally calls pyrofiler.callbacks._DEFAULT_CLB
    """
    _DEFAULT_CLB(*args, **kwargs)

def set_default_callback(clb):
    """
    Configure behaviour of :meth:`pyrofiler.callbacks.default`
    """
    set_default_callback
    global _DEFAULT_CLB
    _DEFAULT_CLB = clb

def enable_printing():
    """ Set default callback to :meth:`pyrofiler.printer` """
    global _DEFAULT_CLB
    _DEFAULT_CLB = printer

def disable_printing():
    """ Set default callback to :meth:`pyrofiler.callbacks.nothing` """
    global _DEFAULT_CLB
    _DEFAULT_CLB = nothing

def append(data, value, **kwargs):
    key = kwargs['description']
    if data.get(key, None) is None:
        data[key] = []
    data[key].append(value)

def assign(data, value, **kwargs):
    key = kwargs['description']
    data[key] = value

def append_to(data):
    def _callback(value, **kwargs):
        append(data, value, **kwargs)
    return _callback

def assign_to(data):
    def _callback(value, **kwargs):
        assign(data, value, **kwargs)
    return _callback
