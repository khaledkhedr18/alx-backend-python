#!/usr/bin/env python3
'''Task 8 - Complex Types: functions'''

from typing import Callable


def make_multiplier(multiplier: float) -> Callable[[float], float]:
    ''' This function takes a multiplier and returns a function
    that multiplies by the multiplier '''
    def multiply(x: float) -> float:
        '''this function multiplies a number by the multiplier '''
        return x * multiplier
    return multiply
