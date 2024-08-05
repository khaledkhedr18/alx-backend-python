#!/usr/bin/env python3

import random
import asyncio


async def wait_random(max_delay: int = 10):
    max_delay = random.randint(0, 10)
    await asyncio.sleep(max_delay)
    return max_delay
