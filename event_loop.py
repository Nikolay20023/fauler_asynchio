import asyncio
from utils import delay

# async def main():
#     await asyncio.sleep(1)

# loop = asyncio.new_event_loop()

# try: 
#     loop.run_until_complete(main())
# finally:
#     loop.close()

def call_later():
    print(f'Меня вызовут в ближащем будущем!')


async def main():
    loop = asyncio.get_running_loop()
    loop.call_soon(call_later)
    await delay(1)

asyncio.run(main(), debug=True)