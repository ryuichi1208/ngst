import concurrent.futures
import os
import math
import sys
import time
import datetime


def benchmark(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start
        print(f"[INFO] func={func.__name__},time={round(elapsed_time, 3)} [s]", result)
        return result

    return wrapper


CALC_LIST = [2, 4, 8]


@benchmark
def test_function_bench_mark(ls: list) -> list:
    ret_list = []
    for i in ls:
        time.sleep(1)
        ret_list.append(i ** i)
    return ret_list


# test_function_bench_mark(CALC_LIST)


def proc_2_calc(ls: list) -> None:
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as executor:
        executor.map(test_function_bench_mark, CALC_LIST)


# proc_2_calc(CALC_LIST)


def _sleep(n: int) -> int:
    time.sleep(n)
    return n


def _calc():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        mappings = executor.submit(_sleep, 1)
        print(mappings.result())


def _current_calcuration(cores: int):
    numbers = [1, 2, 3, 4]
    with concurrent.futures.ProcessPoolExecutor(max_workers=cores) as executor:
        results = executor.map(_sleep, numbers)
        for result in results:
            print(result, datetime.datetime.now())


_current_calcuration(4)
