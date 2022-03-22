from functools import wraps
import sys
import time
from typing import Callable


def timer(function: Callable,
          *args, **kwargs):
    start_time = time.perf_counter()
    function(*args, **kwargs)
    end_time = time.perf_counter()
    print(f'Spend time --{round(end_time - start_time, 5)}s-- '
          f'running function --{function.__name__}-- '
          f'at line --{sys._getframe().f_back.f_lineno}-- '
          f'in file --{__file__.split("/")[-1]}--.')


def timer_decorator(function: Callable):
    @wraps(function)
    def inner(*args, **kwargs):
        start_time = time.perf_counter()
        result = function(*args, **kwargs)
        end_time = time.perf_counter()
        print(f'Spend time --{round(end_time - start_time, 5)}s-- '
              f'running function --{function.__name__}-- '
              f'at line --{sys._getframe().f_back.f_lineno}-- '
              f'in file --{__file__.split("/")[-1]}--.')
        return result

    return inner


class CMTimer(object):
    def __enter__(self):
        self.start_time = time.perf_counter()
        self.start_line = sys._getframe().f_back.f_lineno

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        self.end_line = sys._getframe().f_back.f_lineno
        print(f'Spend time --{round(self.end_time - self.start_time, 5)}s-- '
              f'between line --{self.start_line} to {self.end_line}-- '
              f'in file --{__file__.split("/")[-1]}--.')


if __name__ == '__main__':
    def fun1(n):
        time.sleep(n)

    @timer_decorator
    def fun2(n):
        time.sleep(n)

    def fun3(n):
        time.sleep(n)

    def main():
        timer(fun1, 2)
        fun2(1)
        with CMTimer() as t:
            fun3(1)
        for i in range(1):
            pass
    try:
        from line_profiler import LineProfiler
        lp = LineProfiler(main)
        lp.enable()
        lp.add_function(fun3)
        main()
        lp.disable()
        lp.print_stats(output_unit=1e-3)
    except (ModuleNotFoundError, ImportError):
        main()
