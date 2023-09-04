from aiohttp import ClientSession
from utils import async_timed


async_timed()
async def fetch_status(session: ClientSession, url: str):
    async with session.get(url) as result:
        return result.status