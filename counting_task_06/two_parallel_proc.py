import time 
from multiprocessing import Process

def countdown(n):
    start_time = time.time()
    count = 0
    while count < n:
        count += 1
    end = time.time()
    print(f'Закончен подчсчет до {n} за время {end-start_time} c')
    return count


if __name__ == '__main__':

    start_time = time.time()
    """ это не элегантый способ поскольку процессами мы сами управляем"""

    to_one_hundred = Process(target=countdown, args=(100000000,))
    to_two_hundred = Process(target=countdown, args=(200000000,))

    to_one_hundred.start()
    to_two_hundred.start()

    to_one_hundred.join() # join нужны чтобы не прикончить
    to_two_hundred.join() # дочерние процессы

    end_time = time.time()

    print(f'Полное выполнение работы {end_time - start_time} c')