#!/usr/bin/env python3
'''Task 0's Module
'''
import random
import asyncio


async def wait_random(max_delay: int = 10) -> float:
    '''A function that returns a random waiting number
    '''
    wait_time = random.random() * max_delay
    await asyncio.sleep(wait_time)
    return wait_time
