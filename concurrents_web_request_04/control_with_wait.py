import asyncio
import aiohttp
from aiohttp import ClientSession
from utils import async_timed
from chapter_04 import fetch_status
import logging

# @async_timed()
# async def main():
#     async with aiohttp.ClientSession() as session:
#         fetchers = \
#         [
#             asyncio.create_task(fetch_status(session, 'https://example.com')),
#             asyncio.create_task(fetch_status(session, 'https://example.com'))
#         ]

#         done, pending = await asyncio.wait(fetchers)

#         print(f'Число завершившихся задач: {len(done)}')
#         print(f'Число завершившихся задач: {len(pending)}')

#         for done_task in done:
#             result = await done_task
#             print(result)

@async_timed()
async def main():
    async with aiohttp.ClientSession() as session:
        good_request = fetch_status(session,'https://www.example.com')
        bad_request = fetch_status(session, 'python://bad')

        fetchers = [
            asyncio.create_task(good_request),
            asyncio.create_task(bad_request)
        ]

        done, pending = await asyncio.wait(fetchers)
        print(f'Число завершившихся задач: {len(done)}')
        print(f'Число завершившихся задач: {len(pending)}')

        for done_task in done:
            # result = await done_task возбудит исключение
            if done_task.exception() is None:
                print(done_task.result())
            else:
                logging.error("При выполнение запроса возникло исключение",
                              exc_info=done_task.exception())


asyncio.run(main()) 

