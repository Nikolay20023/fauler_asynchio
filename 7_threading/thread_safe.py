from threading import Lock
from typing import List


class IntListThreadSafe:

    def __init__(self, wrapped_list: List[int]) -> None:
        self._lock = Lock()
        self._inner_list = wrapped_list
    
    def indices_of(self, to_find: int) -> List[int]:
        with self._lock:
            enumerator = enumerate(self._inner_list)
            return [index for index, value in enumerator if value == to_find]
    
    def find_and_replace(self, to_replace, replace_with):
        with self._lock:
            indices = self.indices_of(to_replace)
            for index in indices:
                self._inner_list[index] = replace_with

thraedsafe_list = IntListThreadSafe([1, 2, 1, 2, 1])
thraedsafe_list.find_and_replace(1, 2)