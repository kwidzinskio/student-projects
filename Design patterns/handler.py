'''

At the lecture entitled General patterns of good programming / design discuss several methods for finding the greatest
sum in a contiguous vector sub-interval. Use the Chain of Responsibility design pattern to solve this problem for
vectors of different sizes. For example, a task should first be attempted with a quadratic algorithm, and if it takes
too long, it should be with a linear algorithm.

'''

import abc
import random
import time
from typing import List, Optional


def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f'Execution time: {(end - start) * 1000}ms')
        return result
    return wrapper


class Handler(metaclass=abc.ABCMeta):

    def __init__(self, nxt=None):
        self._nxt = nxt

    def process(self, data: List) -> Optional[int]:
        print(f'Running {self.__class__} algorithm.')
        value = self.handle(data)

        if value is not None:
            print(f'Successfully computed value: {value}')
            return value
        elif self._nxt:
            self._nxt.process(data)
        else:
            print('Unable to compute value. All algorithms failed.')

    @abc.abstractmethod
    def handle(self, data: List) -> Optional[int]:
        pass


class SquareHandler(Handler):
    max_timeout = 1

    @measure_time
    def handle(self, data: List) -> Optional[int]:
        timeout_start = time.time()
        _max = 0

        for i in range(len(data)):
            # This part can be also placed in nested loop (depending on needs)
            if time.time() >= timeout_start + self.max_timeout:
                print(f'Computations took more than {self.max_timeout} seconds. Skipping.')
                return
            _sum = 0
            for x in data[i:]:
                _sum += x
                _max = max(_max, _sum)

        return _max


class LinearHandler(Handler):

    @measure_time
    def handle(self, data: List) -> Optional[int]:
        _max = 0
        _sum = 0
        for x in data:
            _sum = max(_sum + x, 0)
            _max = max(_max, _sum)

        return _max


if __name__ == '__main__':
    n = 10000
    min_range = -100
    max_range = 100

    data = random.choices(range(min_range, max_range), k=n)
    handler = SquareHandler(LinearHandler())
    handler.process(data)

    # test
    print('\nRunning sample tests:')
    test_data = [31, -41, 59, 26, -53, 58, 97, -93, -23, 84]
    assert handler.process(test_data) == 187
    test_data = []
    assert handler.process(test_data) == 0
