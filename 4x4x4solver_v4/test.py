import time
import numpy as np
from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor

def f1(x):
    a, b = x
    return a * b

def f2(a, b):
    return a * b

def main():
    p1 = Pool(4)
    p2 = ProcessPoolExecutor(4)
    a, b = np.random.rand(2, 10**2, 10**2)
    alst = [a+x for x in range(1000)]
    blst = [b+x for x in range(1000)]

    t1 = time.time()
    result1 = p1.map(f1, zip(alst, blst))
    t2 = time.time()
    print("Pool:{:.6f}".format(t2 - t1))

    t1 = time.time()
    result2 = list(p2.map(f2, alst, blst))
    t2 = time.time()
    print("ProcessPoolExecutor:{:.6f}".format(t2 - t1))
    print(np.array_equal(result1, result2))

if __name__ == "__main__":
    main()