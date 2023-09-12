import asyncio
from asyncio import StreamReader
import sys


async def creater_stdin_readrer():
    stream = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(stream)
    loop = asyncio.get_running_loop()
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    return stream
