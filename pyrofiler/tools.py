
def repeat(n):
    def decor(f):
        def wrap(*args, **kwargs):
            for i in range(n):
                x = f(*args, **kwargs)
            return x
        return wrap
    return decor

