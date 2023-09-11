import asyncio
from utils import delay

async def main():
    one_task = asyncio.create_task(delay(3))
    one_two = asyncio.create_task(delay(3))
    one_three = asyncio.create_task(delay(3))
# чтобы совершить сопрограммы конкуретно 
# необходимо сопрограммы обернуть задачами 
    await one_task
    await one_two
    await one_three

asyncio.run(main())