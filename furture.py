from asyncio import Future
import asyncio

from utils import async_timed, delay

# my_future = Future()
# print(f'my_future готов ? {my_future.done()}')
# my_future.set_result(42)
# print(f'my_future готов ? {my_future.done()}')
# print(f'Какой результат хранитс в my_future? {my_future.result()}')

# def make_request():
#     future = Future()
#     asyncio.create_task(set_value_future(future))
#     return future

# async def set_value_future(future: Future):
#     await asyncio.sleep(1)
#     future.set_result(42)

# async def main():
#     future = make_request()
#     print(f'Будущий объект готов? {future.done()}')
#     value = await future
#     print(f'Будущий объект готов? {future.done()}')
#     print(value)

# @async_timed()
# async def delay(sec):
#     print(f'Засыпаю на {sec} c')
#     await asyncio.sleep(sec)
#     print(f'сон в течение {sec} c')
#     return sec

# @async_timed()
# async def main():
#     task_one = asyncio.create_task(delay(2))
#     task_two = asyncio.create_task(delay(3))

#     await task_one
#     await task_two

@async_timed()
async def cpu_bound_work() -> int:
    counter = 0
    for _ in range(1000000):
        counter += 1
    return counter

@async_timed()
async def main():
    task_one = asyncio.create_task(cpu_bound_work())
    task_two = asyncio.create_task(cpu_bound_work())
    task_three = asyncio.create_task(delay(4))

    await task_one
    await task_two
    await task_three

asyncio.run(main())
