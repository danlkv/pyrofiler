import numpy as np
import pyrofiler.c as profilers
import gc
import time

def test_performance():
    N = 50
    S = 400
    estimate_times = [S*S*S/3e9]*N
    estimate_mems = [3*S*S*8]*N
    times = []
    cpus = []
    mems = []
    total_time = 0
    for i in range(N):
        time.sleep(0.01)
        start = time.time()
        with profilers.cpu_util() as prof_cpu:
            with profilers.mem_util() as prof:
                with profilers.timing() as prof_time:
                    A = np.random.rand(S, S)
                    B = np.random.rand(S, S)
                    C = A.dot(B)
        end = time.time()
        times.append(prof_time.result)
        cpus.append(prof_cpu.result)
        mems.append(prof.result)
        del A, B, C
        total_time += end - start

    print('cpus', cpus)

    print('times', times)
    print('estim', estimate_times)
    print('mems', mems)
    print('esti', estimate_mems)

    print()
    print('total time', total_time)
    print('payload time', sum(times))
    assert sum(times)-total_time < N*0.005

if __name__ == "__main__":
    test_performance()

