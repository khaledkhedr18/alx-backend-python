#!/usr/bin/env python3

'''Task 0' Module
'''


import asyncio
import random


async def wait_random(max_delay: int = 10) -> float:
    ''' A function that returns a random waiting number
    '''
    waitingTime = random.random() * max_delay
    await asyncio.sleep(waitingTime)
    return waitingTime


print(asyncio.run(wait_random()))
print(asyncio.run(wait_random(5)))
print(asyncio.run(wait_random(15)))
