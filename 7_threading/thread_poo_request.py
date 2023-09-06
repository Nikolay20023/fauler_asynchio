import requests
import asyncio
from utils import async_timed

def get_status_code(url: str) -> int:
    response = requests.get(url)
    return response.status_code


@async_timed()
async def main():
    urls = ['https://www.example.com' for _ in range(10)]
    tasks = [asyncio.to_thread(get_status_code, url) for url in urls]
    result = await asyncio.gather(*tasks)
    print(result)
asyncio.run(main())



