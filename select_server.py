import selectors
import socket
from selectors import SelectorKey
from typing import List, Tuple


selector = selectors.DefaultSelector() # Инициализируем класс для работы с библиотекой select
server_socket = socket.socket() # инициализация сокета 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

# socket.AF_INET тип адреса содержащий хост порт
# socket.SOL_SOCKET возвращает значения указывающее находится в режиме прослушивания 

# socket.SO_REUSEADDR позволяет повторно использовать номер порта 


server_address = ('127.0.0.1', 8000)
server_socket.setblocking(False)
server_socket.bind(server_address)

server_socket.listen()

# регистрация сокета для библиотеки select для чтения 
selector.register(server_socket, selectors.EVENT_READ)  

while True:
    events: List[Tuple[SelectorKey, int]] = selector.select(timeout=1)

    if len(events) == 0: # Если ничего не произошло значит так и выводить сообщение
        print('Событий нет, подожду')
    
    for event, _ in events:
        event_socket = event.fileobj

        if event_socket == server_socket:
            connection, address = server_socket.accept()
            connection.setblocking(False)
            print(f'Получен запрос на подключение от {address}')
            selector.register(connection, selectors.EVENT_READ)

        else:
            data = event_socket.recv(1024)
            print(f'Получены данные: {data}')
            event_socket.send(data)
