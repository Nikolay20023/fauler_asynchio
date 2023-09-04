import socket 
import asyncio
from types import TracebackType
from typing import Optional, Type
from utils import timer

class ConnectionSocket:

    def __init__(self, serve_socket) -> None:
        self._serve_socket = serve_socket
        self._connection = None
    
    async def __aenter__(self):
        print('Вход в контекстный менеджер')
        loop = asyncio.get_event_loop()
        connetion, address = await loop.sock_accept(self._serve_socket)
        self._connection = connetion
        print(f'Подключение подтверждено :{address}')
        return self._connection
    
    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType]
    ):
        print('Выход из контекстного менеджера')
        self._connection.close()
        print('Подключение закыто')
    

async def main():
    loop = asyncio.get_event_loop()
    serve_socket = socket.socket()
    serve_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serve_socket.setblocking(False)
    address = ('127.0.0.1', 8000)
    serve_socket.bind(address)

    serve_socket.listen()

    async with ConnectionSocket(serve_socket) as connection:
        data = await loop.sock_recv(connection, 1024)
        print(data)


asyncio.run(main())
