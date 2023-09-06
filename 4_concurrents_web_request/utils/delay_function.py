import asyncio


async def delay(delay_second: int):
    print(f'засыпаю {delay_second} с')
    await asyncio.sleep(delay_second)
    print(f'сон в течении {delay_second} с закончился')
    return delay_second