# from utils.delay_function import delay
# from utils.timer import async_timed
import asyncio
import sys

async def delay(delay_second: int):
    print(f'засыпаю {delay_second} с')
    await asyncio.sleep(delay_second)
    print(f'сон в течении {delay_second} с закончился')
    return delay_second


async def creater_stdin_readrer():
    stream = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(stream)
    loop = asyncio.get_running_loop()
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    return stream
