#!/usr/bin/env python3
'''Task 7: Complex Types'''

from typing import Tuple, Union


def to_kv(k: str, v: Union[int, float]) -> Tuple[str, float]:
    ''' This function takes a key and a value
    and returns a tuple of the key and value '''
    return (k, v ** 2)
