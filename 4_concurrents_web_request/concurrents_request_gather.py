import asyncio
import aiohttp
from aiohttp import ClientSession
from chapter_04 import fetch_status
from utils import async_timed

@async_timed()
async def main():
#  приятная особенность использрования gather 
#  является то что она детерминирована не важна какая сопрограмма завершится первой 
#  они придут в таком порядке в котором их запустили
#     
    async with aiohttp.ClientSession() as session:
        urls = ['https://example.com' for _ in range(1000)]
        requests = [fetch_status(session, url) for url in urls]
        status_code = await asyncio.gather(*requests)
        print(status_code)

asyncio.run(main())