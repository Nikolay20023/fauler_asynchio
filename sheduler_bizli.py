import logging 
from typing import Generator, Union
from queue import Queue
import types
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

logger = logging.getLogger(__name__)



class Task:
    task_id = 0

    def __init__(self, target: Generator) -> None:
        Task.task_id += 1
        self.tid = Task.task_id
        self.target = target
        self.stack = []
        self.sendval = None

    
    def run(self):
        while True:
            try:
                result = self.target.send(self.sendval)

                if isinstance(result, types.GeneratorType):
                    self.stack.append(self.target)
                    self.sendval = None
                    self.target = result

                else:
                    if not self.stack:
                        return
                    self.sendval = result
                    self.target = self.stack.pop

            except StopIteration:
                if not self.stack:
                    raise
                self.sendval = None
                self.target = self.stack.pop()


class Scheduler:
    def __init__(self):
        self.ready = Queue()
        self.task_map = {}
        self.selector = DefaultSelector()

    def add_task(self, coroutine: Generator) -> int:
        new_task = Task(coroutine)
        self.task_map[new_task.tid] = new_task
        self.schedule(new_task)
        return new_task.tid

    def exit(self, task: Task):
        logger.info('Task %d terminated', task.tid)
        del self.task_map[task.tid]

    def wait_for_read(self, task: Task, fd: int):
        try:
            key = self.selector.get_key(fd)
        except KeyError:
            self.selector.register(fd, EVENT_READ, (task, None))
        
        else:
            mask, (reader, writer) = key.events, key.data
            self.selector.modify(fd, mask | EVENT_READ, (task, writer))
    
    def _remove_reader(self, fd: int):
        try:
            key = self.selector.get_key(fd)
        except KeyError:
            pass
        
        else:
            mask, (reader, writer) = key.events, key.data
            mask &= ~EVENT_READ

            if not mask:
                self.selector.unregister(fd)
            else:
                self.selector.modify(fd, mask, (None, writer))

    def _remove_writer(self, fd: int):
        try:
            key = self.selector.get_key(fd)
        except KeyError:
            pass

        else:
            mask, (reader, writer) = key.events, key.data
            mask &= ~EVENT_WRITE

            if not mask:
                self.selector.unregister(fd)
            else:
                self.selector.modify(fd, mask, (reader, None))

    def io_poll(self, timeout: Union(None, float)):
        events = self.selector.select(timeout)
        



    def schedule(self, task: Task):
        self.ready.put(task)

    def _run_once(self):
        task = self.ready.get()
        try:
            result = task.run()
        except StopIteration:
            self.exit(task)
            return
        self.schedule(task)

    def event_loop(self):
        while self.task_map:
            self._run_once()


def double(x):
    yield x * x

def add(x, y):
    yield from double(x + y)

def main():
    result = yield add(1, 2)
    print(result)
    yield

a = main()

task = Task(a)
task.run()