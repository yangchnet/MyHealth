from socket import *
import threading
HOST = 'localhost'
PORT = 21578
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpClisock = socket(AF_INET, SOCK_STREAM)
tcpClisock.connect(ADDR)

tem = '1,ID:10101010,TEMP=35.45'
oxygen = '2,ID:20202020,HR=123,HRvalid=1,SPO2=321,SPO2valid=1'
heart = '3,ID=30303030,B=234,Q=345,S=456'
pressure = '4,ID=40404040,BPSS=345,BPSZ=577'

# class Send(threading.Thread):
#     def __init__(self, tcpClisock, data):
#         super(Send, self).__init__()
#         self.tcpClisock = tcpClisock
#         self.data = data
#
#     def run(self):
#         while True:
#             if not self.data:
#                 break
#             # tcpClisock.connect(ADDR)
#             tcpClisock.send(self.data.encode())
#             print('send:%s'%self.data)
#
# send1 = Send(tcpClisock, tem)
# send2 = Send(tcpClisock, oxygen)
# send3 = Send(tcpClisock, heart)
# send4 = Send(tcpClisock, pressure)
#
# send2.start()
# send1.start()
#
# send3.start()
# send4.start()
data = oxygen
while True:
    if not data:
        break
    tcpClisock.send(data.encode())
    data = tcpClisock.recv(BUFSIZ)
    if not data:
        break
    print(data)

