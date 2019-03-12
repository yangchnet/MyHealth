from socket import *
import threading
from time import ctime

HOST = ''
POST = 21578
BUFSIZ = 1024
ADDR = (HOST, POST)
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(50)

class Recv(threading.Thread):
    def __init__(self, tcpCliSock):
        super(Recv, self).__init__()
        # print('waiting for connection...')
        # tcpCliSock, addr = tcpSerSock.accept()
        # print('...connected from:', addr)
        self.tcpCliSock = tcpCliSock

    def run(self):
        while True:
            data = self.tcpCliSock.recv(BUFSIZ)
            # data = str(data, encoding = "utf-8")
            if not data:
                break
            print(data)
            self.tcpCliSock.send(b'you have send a message:' + data)



while True:
    print('waiting for connection...')
    tcpCliSock, addr = tcpSerSock.accept()
    print('...connected from:', addr)

    recv = Recv(tcpSerSock)
    recv.start()

tcpSerSock.close()
