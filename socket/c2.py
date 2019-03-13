from socket import *
import threading
import time

HOST = 'localhost'
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpClisock = socket(AF_INET, SOCK_STREAM)
tcpClisock.connect(ADDR)

tem = '1,ID:10101010,TEMP=22.22'
oxygen = '2,ID:10101010,HR=123,HRvalid=1,SPO2=321,SPO2valid=1'
heart = '3,ID:10101010,B=234,Q=345,S=456'
pressure = '4,ID:10101010,BPSS=345,BPSZ=577'

data = tem
i = 0
while i<10:
    if i == 9:
        tcpClisock.send(data.encode())
    if not data:
        break
    tcpClisock.send(data.encode())
    i += 1
    # rdata = tcpClisock.recv(BUFSIZ)
    # if not rdata:
    #     break
    # print(rdata)
    time.sleep(2)

