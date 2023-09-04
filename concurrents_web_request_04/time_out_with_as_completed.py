import asyncio
import aiohttp
from aiohttp import ClientSession
from utils import async_timed
from chapter_04 import fetch_status

# Проблема в том что если мы хотим снять задачу
# то мы не понимаем какую именно нужно снять задачу 
# потому что в as_completed недетерминированный порядок получения результата задачи 

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        fetchers = [
            fetch_status(session, 'https://www.example.com', 1),
            fetch_status(session, 'https://www.example.com', 10),
            fetch_status(session, 'https://www.example.com', 10)
        ]

        for done_task in asyncio.as_completed(fetchers, timeout=3):
            try:
                result = await done_task
                print(result)
            except asyncio.TimeoutError:
                print(f'Произошёл таймаут')
        
        for task in asyncio.tasks.all_tasks():
            print(task)

asyncio.run(main())