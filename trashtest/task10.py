#!/usr/bin/env python3
'''Task 10 - first element of a sequence'''

from typing import Sequence, Union, Any


def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    ''' This function returns the first element of a sequence if it exists '''
    if lst:
        return lst[0]
    else:
        return None
