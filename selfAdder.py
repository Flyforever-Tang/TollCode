import sys


class SelfAdder(object):
    MAX_INT = sys.maxsize

    def __init__(self,
                 start: int = 0,
                 maximum: int = MAX_INT):
        self.i = start
        self.maximum = maximum

    def __call__(self):
        if self.i == self.maximum:
            self.i = 1
        else:
            self.i = self.i + 1

        return self.i - 1


if __name__ == '__main__':
    adder = SelfAdder()
    print(adder())
    print(adder())
    print(adder())
    print(adder())
    print(adder())
    print(adder())

    adder = SelfAdder(maximum=3)
    print(adder())
    print(adder())
    print(adder())
    print(adder())
    print(adder())
    print(adder())
