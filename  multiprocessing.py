import time 
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

def count(num) -> int:
    start_at = time.time()
    counter = 0
    while counter < num:
        counter += 1

    end = time.time()
    print(f'Функция Завершилось всё за {end - start_at} c')
    return counter

if __name__ == '__main__':
    # start_time = time.time()
    
    # one = multiprocessing.Process(target=count, args=(100000000, ))
    # two = multiprocessing.Process(target=count, args=(200000000, ))

    # one.start()
    # two.start()

    # one.join()
    # two.join()

    # end = time.time()
    start_time = time.time()

    with ProcessPoolExecutor() as process_pool:
        numbers = [1, 3, 5, 22, 100000000]
        for result in process_pool.map(count, numbers):
            print(result)
    
    end = time.time()
    print(f'Основной поток завершился {end - start_time}')

