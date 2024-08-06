#!/usr/bin/env python3
'''Task 0's Module'''

import random
import asyncio
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    ''' A function that loops 10 times, each time waits 1 second
    Then yield a random number between 0 and 10'''
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.uniform(0, 10)
