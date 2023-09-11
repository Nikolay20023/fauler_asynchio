import asyncio
from utils import delay

async def add_one(number: int) -> int:
    return number + 1

async def hello_world():
    await delay(1)
    return 'Hello world'

async def main():
    message = await hello_world()
    one_plus_one = await add_one(1)
    print(one_plus_one)
    print(message)

asyncio.run(main())