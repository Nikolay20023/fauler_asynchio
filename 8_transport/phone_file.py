import asyncio
from fauler_asynchio.utils import delay
from fauler_asynchio.utils import creater_stdin_readrer

async def main():
    stdin = await creater_stdin_readrer()
    while True:
        delay_time = await stdin.readline()
        asyncio.create_task(delay(delay_time))

asyncio.run(main())
