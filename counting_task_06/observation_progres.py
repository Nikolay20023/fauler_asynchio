from concurrent.futures import ProcessPoolExecutor
import functools
import asyncio
from multiprocessing import Value
from typing import List, Dict
from asynco_reduce import partions, merge_dictionares

map_progress: Value

def init(progress: Value):
    global map_progress
    map_progress = progress

def map_frequencies(chunk: List[str]) -> Dict[str, int]:
    counter = 0
    for line in chunk:
        word, _, count, _ = line.split('\t')
        if counter.get(word):
            counter[word] = counter[word] + int(count)
        else:
            counter[word] = int(count)
        
        with map_progress.get_lock():
            map_progress.value += 1
        
    return counter

async def progress_reporter(total_partitions: int):
    while map_progress.value < total_partitions:
        print(f'Завершено операции отображений:{map_progress.value}/{total_partitions}')
        await asyncio.sleep(1)

async def main(pertitions_size: int):
    global map_progress

    with open('/home/nikolay20023/sprint3/counting_task_06/googlebooks-eng-all-1gram-20120701-a', encoding='utf-8') as f:
        contents = f.readlines()
        loop = asyncio.get_running_loop()
        tasks = []
        map_progress = Value('i', 0)

        with ProcessPoolExecutor(initializer=init, initargs=(map_progress, )) as pool:
            total_partions = len(contents) // pertitions_size
            reporter = asyncio.create_task(progress_reporter(total_partions))

            for chunk in partions(contents, pertitions_size):
                tasks.append(
                    loop.run_in_executor(
                        pool,
                        functools.partial(map_frequencies, chunk)
                    )
                )
            
            counter = await asyncio.gather(**tasks)

            await reporter
            final_result = functools.reduce(merge_dictionares, counter)
            print(f"Aardvark встречается {final_result['Aardvark']} раз.")


if __name__ == '__main__':
    asyncio.run(main(pertitions_size=60000))
