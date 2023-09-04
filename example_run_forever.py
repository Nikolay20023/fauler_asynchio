import asyncio
import time 


async def delay(second):
    print(f'Засыпаю на {second} c')
    second = await asyncio.sleep(second)
    print(f'Конец сна {second}')
    return second


async def main():
    begin = time.time()
    one = asyncio.create_task(delay(3))
    two = asyncio.create_task(delay(3))
    third = asyncio.create_task(delay(3))

    await one
    await two
    await third
    print(f'Прошло времени: {time.time() - begin}')

asyncio.run(main())