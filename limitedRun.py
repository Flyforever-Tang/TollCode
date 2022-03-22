from typing import Any


class LimitedRun(object):
    run_dict = {}

    def __init__(self,
                 tag: Any = 'default',
                 limit: int = 1):
        self.tag = tag
        self.limit = limit

    def __enter__(self):
        if self.tag in LimitedRun.run_dict.keys():
            LimitedRun.run_dict[self.tag] += 1
        else:
            LimitedRun.run_dict[self.tag] = 1
        return LimitedRun.run_dict[self.tag] <= self.limit

    def __exit__(self, exc_type, exc_value, traceback):
        return


if __name__ == '__main__':
    a = 0
    for i in range(3):
        with LimitedRun('print_1', 4) as limited_run:
            if limited_run:
                print(1, type(a))
        a += 1
    for i in range(3):
        with LimitedRun('print_1', 4) as limited_run:
            if limited_run:
                print(2, type(a))
        a += 1
    print(a)
