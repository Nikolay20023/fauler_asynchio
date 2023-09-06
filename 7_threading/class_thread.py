from threading import Thread
import socket

class ClientEchoThread(Thread):

    def __init__(self, client):
        super().__init__()
        self._client = client

    def run(self):
        try:
            while True:
                data = self._client.recv(2048)
                if not data:
                    raise BrokenPipeError('Подключение закрыто')
                print(f'Получены данные {data}, отправляю')
                self._client.sendall(data)
        except OSError as e:
            print(f'Поток прерван исключением {e}, производится остановка')

    def close(self):
        if self.is_alive():
            self._client.sendall(bytes('Останавливаюсь', encoding='utf-8'))
            self._client.shutdown(socket.SHUT_RDWR)
    
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 8000))
    server.listen()
    connection_thread = []

    try:
        while True:
            connection, address = server.accept()
            thread = ClientEchoThread(connection)
            connection_thread.append(thread)
            thread.start()
    except KeyboardInterrupt:
        print('Остановитесь')
        [th.close for th in connection_thread]