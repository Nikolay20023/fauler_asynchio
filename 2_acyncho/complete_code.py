import asyncio
from utils import delay

async def hello_every_seond():
    for i in range(2):
        await asyncio.sleep(1)
        print("Пока я жду , исполняется другой код")

async def main():
    first_delay = asyncio.create_task(delay(3))
    second_delay = asyncio.create_task(delay(3))
    await hello_every_seond()
    await first_delay
    await second_delay

asyncio.run(main())