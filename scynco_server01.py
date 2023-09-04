import socket

serve_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serve_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

serve_address = ('127.0.0.1', 8000)
serve_socket.bind(serve_address)
serve_socket.listen()
serve_socket.setblocking(False)
connections = []

try:
    while True:

        try:
            connection, client_address = serve_socket.accept()
            connection.setblocking(False)
            print(f'Получен запрос на подключение от {client_address}!')
            connections.append(connection)
        except BlockingIOError:
            
            pass

        for connection in connections:
            try:
                buffer = b''

                while buffer[-2:] != b'\r\n':
                    data = connection.recv(2)
                    if not data:
                        break
                    else:
                        print(f'Полученны данные: {data}!')
                        buffer = buffer + data

                print(f'Все данные: {buffer}!')
                connection.send(buffer)
            except BlockingIOError:
                pass
finally:
    serve_socket.close()