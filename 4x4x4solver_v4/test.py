import select
import socket

def slow_syscall(timeout=1):
    """遅いシステムコールを実行する関数"""
    select.select([socket.socket()], [], [], timeout)

def factorize(number):
    """素因数分解する関数"""
    for i in range(1, number + 1):
        if number % i == 0:
            yield i

def call_factorize(number):
    """イテレーターをリストに変換する"""
    return list(factorize(number))

from time import time
from concurrent.futures import ProcessPoolExecutor

numbers = [53541233, 21235343, 11421443, 5423123]
start = time()

with ProcessPoolExecutor(max_workers=2) as pool:
    # mapは呼び出す関数をイテラブルな要素それぞれに対して実行する。
    results = pool.map(call_factorize, numbers)

    for result in results:
        print(result)

print('Took %.3f seconds' % (time() - start))