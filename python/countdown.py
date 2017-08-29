#!/usr/bin/env python
# coding=utf-8
from __future__ import print_function

import operator
import sys


operators = [
    operator.add,
    operator.sub,
    operator.mul,
    operator.div,
    # pow
]

COUNT = 0
TRIED = {}
FORMULAS = []


def num_to_key(numbers):
    return ','.join(map(str, numbers))


def naive(numbers, target):
    numbers.sort()
    if len(numbers) == 1 and numbers[0]:
        if numbers[0] != target:
            return False

    global COUNT
    COUNT += 1
    global TRIED
    key = num_to_key(numbers)
    if key in TRIED:
        return False
    TRIED[key] = True

    for m, number_a in enumerate(numbers):
        if number_a == target:
            return True
        for n, number_b in enumerate(numbers):
            if m == n:
                continue
            for op in operators:
                if op == operator.div and number_a % number_b != 0:
                    continue
                result = op(number_a, number_b)
                if result <= 0:
                    continue

                # create a copy, remove used numbers, and add result
                rest = numbers[:]
                rest.pop(m if m > n else n)
                rest.pop(n if m > n else m)
                rest.append(result)

                if naive(rest, target):
                    global FORMULAS
                    FORMULAS.insert(0, (number_a, op, number_b))
                    return True
    return False


def countdown(target, nums):
    assert target > 0
    if naive(nums, target):
        print('Found the target in {} tries ({} unique)'.format(COUNT, len(TRIED)), end='\n\n')
        for a, op, b in FORMULAS:
            print('{} {} {} = {}'.format(a, op.__name__, b, op(a, b)))
    else:
        print('Could not find the target in {} tries ({} unique)'.format(COUNT, len(TRIED)))


if __name__ == '__main__':
    countdown(int(sys.argv[2]), map(int, sys.argv[1].split(',')))
