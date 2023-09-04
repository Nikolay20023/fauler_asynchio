import socket
import selectors
import logging
import sys
import time 


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

def new_connection(selector: selectors.BaseSelector, sock: socket.socket):
    new_conn, addr = sock.accept()
    new_conn.setblocking(False)
    selector.register(new_conn, selectors.EVENT_READ, read_callback)

def read_callback(selector: selectors.BaseSelector, sock: socket.socket):
    data = sock.recv(1024)
    print(data.decode())
    command = data.decode().strip()

    if command == 'exit':
        logger.info('closing connection %s', sock)
        selector.unregister(sock)
        sock.close
    
    elif command == 'time':
        logger.info('time %s', sock)
        sock.send(str(time.time()).encode)

    elif data:
        sock.send('Hello pidor'.encode())

def run_iterations(selector: selectors.BaseSelector):
    events = selector.select()
    for key, mask in events:
        callback = key.data
        callback(selector, key.fileobj)

HOST, PORT = '', 12345

if __name__ == '__main__':

    with selectors.SelectSelector() as selector:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
            serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
            serv_sock.bind((HOST, PORT))
            serv_sock.listen()
            serv_sock.setblocking(False)

            selector.register(serv_sock, selectors.EVENT_READ, new_connection)

            while True:
                run_iterations(selector)


        