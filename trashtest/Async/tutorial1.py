# create the function fetch data
#create the main function with 3 tasks
# run the main function


import asyncio

async def fetch_data(id, delay):
    print(f"Coroutine with id: {id}, is starting to fetch the data")
    await asyncio.sleep(delay)
    return f"Coroutine with id: {id}, has fetched the data"

async def main():
    print("Starting the main coroutine")
    task1 = asyncio.create_task(fetch_data(1, 2))
    task2 = asyncio.create_task(fetch_data(2, 3))
    task3 = asyncio.create_task(fetch_data(3, 1))

    result1 = await task1
    result2 = await task2
    result3 = await task3

    print(result1, result2, result3)

asyncio.run(main())
