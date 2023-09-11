import asyncio

async def add_one(number: int) -> int:
    return number + 1

async def main():
    one_plus_one = await add_one(1)
    two_lus_one = await add_one(2)

    print(one_plus_one)
    print(two_lus_one)

asyncio.run(main())