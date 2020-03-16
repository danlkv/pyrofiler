import pyrofiler

@pyrofiler.cpu_util(description='Cpu usage')
@pyrofiler.timed('Time elapsed')
def sum_series(x, N):
    return sum([x**i/i for i in range(1, N)])

sum_series(.3, 1000_000)
