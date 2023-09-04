import asyncio
import aiohttp
from aiohttp import ClientSession
from chapter_04 import fetch_status
from utils import async_timed
from utils  import delay


@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        urls = ['https://example.com' for _ in range(1000)]
        requests = [fetch_status(session, url) for url in urls]
        status_code = await asyncio.gather(*requests)
        print(status_code)


# async def main():
#     results = await asyncio.gather(delay(3), delay(1))
#     print(results)

asyncio.run(main())