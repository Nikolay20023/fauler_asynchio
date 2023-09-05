import time 
import asyncio
import functools
import concurrent.futures
from typing import List, Dict

# Сначала шинкуем данные для более мелкие чтобы лечге было переварить 
# c помощью генератора 
def partions(data: List, chunk_size: int) -> List:
    for i in range(0, len(data), chunk_size):
        yield data[i: i + chunk_size]

# Функция map_frequencies производит подсчёт слов 
# по стандартному алгоритму 
def map_frequencies(chunk: List[str]):
    counter = {}
    for line in chunk:
        word, _, count, _ = line.split('\t')
        if counter.get(word):
            counter[word] += int(count)
        else:
            counter[word] = int(count)
        
    return counter

# Здесь мы производим слияние 
def merge_dictionares(first: Dict[str, int], second: Dict[str, int]) -> Dict:
    merged = first
    for key in second:
        if key in merged:
            merged[key] = merged[key] + second[key]
        else:
            merged[key] = second[key]
    
    return merged

async def reduce(loop, pool, counters, chunk_size) -> Dict[str, int]:
    chunks: List[List[Dict]] = list(partions(counters, chunk_size))
    reducers = []
    for chunk in chunk_size:
        reducer = functools.partial(functools.reduce, 
                                    merge_dictionares, chunk)
        reducers.append(loop.run_in_executor(pool, reducer))
        reducer_chunk = await asyncio.gather(*reducer)
        chunks = list(partions(reducer_chunk, chunk))
        reducers.clear()
    return chunks[0][0]



async def main(partition_size: int):
    with open(
        '/home/nikolay20023/sprint3/counting_task_06/googlebooks-eng-all-1gram-20120701-a',
        encoding='utf-8'
    ) as f:
        contents = f.readlines() # чтение 
        loop = asyncio.get_running_loop()
        tasks = []
        start = time.time()
        with concurrent.futures.ProcessPoolExecutor() as pool: # С помощью пула процессов 
            for chunk in partions(contents, partition_size):   # создаём маленьки порции 
                tasks.append(                                  # добавляем в цикл 
                    loop.run_in_executor(                      # связываем с partial 
                        pool,
                        functools.partial(
                            map_frequencies,
                            chunk
                        )
                    )
                )
            intermediate_results = await asyncio.gather(*tasks) # дожидаемся результата c спомощью gather 
            final_result = functools.reduce(merge_dictionares,
                                            intermediate_results) # в итоге редуцируем 
            print(f"Aarfvark встречается {final_result['Aardvark']} раз")
            end = time.time()
            print(f'Время MapReduce: {end - start:.4f} секунд')

if __name__ == '__main__':
    asyncio.run(main(partition_size=6000))