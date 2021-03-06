import pickle
import socket
import time


MAX_CONNECTIONS = 1
address_to_server = ('localhost', 8686)

clients = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for i in range(MAX_CONNECTIONS)]
for client in clients:
    client.connect(address_to_server)

for i in range(MAX_CONNECTIONS):
    clients[i].send(bytes("hello from client number " + str(i), encoding='UTF-8'))

for client in clients:
    data = client.recv(1024)
    print(str(data))
    data_arr = pickle.loads(data)
    sock.close()
    print(repr(data_arr))