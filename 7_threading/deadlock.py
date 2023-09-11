from threading import Lock
import time

lock_a = Lock()
lock_b = Lock()

def a():
    with lock_a:
        print('Захвачена блокирвки a из метода a!')