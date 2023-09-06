import asyncio
import aiohttp
from aiohttp import ClientSession
from ..utils import async_timed


@async_timed()
async def fetch_status(session: ClientSession, url: str) -> int:
    async with session.get(url) as sess:
        return sess.status()


@async_timed()
async def main():
    async with aiohttp.ClientSession() as sess:
        url = 'https://www.example.com'
        status = await fetch_status(sess, url)
        print(f'Состояние для {url} было равно {status}')

asyncio.run(main())

