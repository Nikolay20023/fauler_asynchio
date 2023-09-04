import socket
import asyncio, signal
import logging
from asyncio import AbstractEventLoop
from typing import List

from utils.delay_function import delay


async def echo(
        connection: socket,
        loop: AbstractEventLoop
):
    try:
        while data := await loop.sock_recv(connection, 1024):
            print('got data')
        if data == b'boom\r\n':
            raise Exception("Неожиданная ошибка сети")
        await loop.sock_sendall(connection, data)
    except Exception as ex:
        logging.exception(ex)
    finally:
        connection.close()
    
echo_task = []

async def listen_for_connetcion(server_socket: socket, loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f'Получен запрос на подключение {address}')
        task = asyncio.create_task(echo(connection, loop))
        echo_task.append(task)

class GracefulExit(SystemExit):
    pass

def shutdown():
    raise GracefulExit()

async def close_echo_tasks(echo_tasks: List[asyncio.Task]):
    waiters = [asyncio.wait_for(task, 2) for task in echo_task]
    for task in waiters:
        try:
            await task
        except asyncio.exceptions.TimeoutError:
            pass

async def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)

    server_socket.listen()

    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(getattr(signal, signame), shutdown)
    await listen_for_connetcion(server_socket, loop)


loop = asyncio.new_event_loop()

try:
    loop.run_until_complete(main())
except GracefulExit:
    loop.run_until_complete(close_echo_tasks(echo_task))
finally:
    loop.close()


        