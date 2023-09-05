from multiprocessing import Pool

def say_hello(name: str) -> str:
    return f'Hello {name}!'

if __name__ == '__main__':
    with Pool() as process_pool:
        # hi_jeff = process_pool.apply(say_hello, args=('JEff', ))
        # hi_john = process_pool.apply(say_hello, args=('john', ))
        hi_jeff = process_pool.apply_async(say_hello, args=('JEff', ))
        hi_john = process_pool.apply_async(say_hello, args=('john', ))
        print(hi_jeff.get())
        print(hi_john.get())