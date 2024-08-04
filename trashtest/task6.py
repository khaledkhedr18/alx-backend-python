#!/usr/bin/env python3
'''Task 6: mixed list'''

from typing import List, Union


def sum_mixed_list(mxd_list: List[Union[int, float]]) -> float:
    ''' This function sums a list of mixed types '''
    return sum(mxd_list)
