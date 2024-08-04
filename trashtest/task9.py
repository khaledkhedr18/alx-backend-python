#!/usr/bin/env python3
'''Task 9 - Duck Typing'''

from typing import List, Tuple, Sequence, Iterable


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    ''' This function returns a list of tuples '''
    return [(i, len(i)) for i in lst]
