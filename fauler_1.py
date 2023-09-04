import asyncio
from utils import delay
from asyncio import CancelledError

async def add_one(num: str):
    return num + 1

async def hello_world() -> str:
    await delay(1)
    return 'Hello world'

async def hello_every_second():
    for i in range(2):
        await asyncio.sleep(1)
        print('пока я жду , исполняется другой код!')

"""Конкуретное использования программ"""

# async def main():
#     first_delay = asyncio.create_task(delay(3))
#     second = asyncio.create_task(delay(3))
#     # sleep_once_more = asyncio.create_task(delay(3))

#     await hello_every_second()
#     await first_delay
#     await second

# async def main():
#     long_task = asyncio.create_task(delay(10))

#     second_elapsed = 0

#     while not long_task.done():
#         print('Задача не закончилпась, слеующая проверка через секунду.')
#         await asyncio.sleep(1)
#         second_elapsed = second_elapsed + 1
#         if second_elapsed == 5:
#             long_task.cancel() 
    
#     try:
#         await long_task
#     except CancelledError:
#         print('Наша задача была снята ')

# async def main():
#     delay_task = asyncio.create_task(delay(2))
#     try:
#         result = await asyncio.wait_for(delay_task, timeout=1)
#         print(result)
#     except asyncio.exceptions.TimeoutError:
#         print('Тайм-аут')
#         print(f'Задача была снята {delay_task.cancelled()}')

async def main():
    task = asyncio.create_task(delay(10))

    try: 
        result = await asyncio.wait_for(asyncio.shield(task), 5)
        print(result)
    except asyncio.exceptions.TimeoutError:
        print('Задача заняла более 5 c , скоро она закончится ')
        result = await task
        print(result)

asyncio.run(main())