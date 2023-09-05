from multiprocessing import Value, Array, Process

def increment_value(shared_int: Value):
    shared_int.value = shared_int.value + 1

def increment_array(shared_array: Array):
    for index, integer in enumerate(shared_array):
        shared_array[index] = integer + 1
    
if __name__ == '__main__':
    # intger = Value('i', 0)
    # integr_array = Array('i', [0, 0])

    # procs = [
    #     Process(target=increment_value, args=(intger, )),
    #     Process(target=increment_array, args=(integr_array, ))
    # ]
    # [p.start for p in procs]
    # [p.join for p in procs]

    # print(intger.value)
    # print(integr_array[:])
    for _ in range(100):
        integer = Value('i', 0)
        procs = [
            Process(target=increment_value, args=(integer, )),
            Process(target=increment_value, args=(integer, ))
        ]

        [p.start() for p in procs]
        [p.join() for p in procs]
        print(integer.value == 2)
