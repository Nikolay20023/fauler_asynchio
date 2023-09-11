import asyncio

async def hello_world() -> str:
    await asyncio.sleep(1)
    return 'Hello world'

async def main():
    message = await hello_world()
    print(message)

asyncio.run(main())