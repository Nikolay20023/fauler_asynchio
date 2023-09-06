import asyncio
from ..utils import delay, async_timed

@async_timed()
async def main() -> None:
    delay_times = [3, 3, 3]
    tasks = [asyncio.create_task(delay(second)) for second in delay_times]
    [await task for task in tasks]

asyncio.run(main())