#!/usr/bin/env python3
'''Task 1's Module'''

import asyncio
import random
from typing import List
async_generator = __import__('0-async_generator').async_generator


async def async_comprehension() -> List[float]:
    ''' A function that returns a list of random numbers
    '''
    return [i async for i in async_generator()]
