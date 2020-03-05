
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
