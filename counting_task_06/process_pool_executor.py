import time 
from concurrent.futures import ProcessPoolExecutor

def countdown(n):
    start = time.time()
    count = 0
    while count < n:
        count += 1
    end = time.time()
    print(f'Закончен подсчет до {n} за {end - start} c')


if __name__ == '__main__':
    with ProcessPoolExecutor() as pool:
        numbers = [1, 3, 5, 100000000]
        for result in pool.map(countdown, numbers):
            print(result)