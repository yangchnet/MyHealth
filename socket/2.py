from socket import *
import threading
from time import ctime

HOST = ''
POST = 21576
BUFSIZ = 1024
ADDR = (HOST, POST)
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

class Recv(threading.Thread):
    def __init__(self, tcpCliSock):
        super(Recv, self).__init__()
        self.tcpCliSock = tcpCliSock

    def run(self):
        while True:
            data = self.tcpCliSock.recv(BUFSIZ)
            # data = str(data, encoding = "utf-8")
            if not data:
                break
            self.tcpCliSock.send(b'you have send a message:' + data)
            print(data)


while True:
    print('waiting for connection...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('...connected from:', addr)

    recv = Recv(tcpCliSock)
    recv.start()

tcpSerSock.close()
