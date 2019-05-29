# from socket import AF_INET, SOCK_STREAM
import socket
socket.has_ipv6
import time
import threading
HOST = '2001:da8:270:2020:f816:3eff:fe93:b159'
PORT = 7001
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpClisock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpClisock.connect(ADDR)

tem = '1,ID:10101010,TEMP=35.45'
oxygen = '2,ID:10101010,HR=888,HRvalid=1,SPO2=321,SPO2valid=1'
heart = '3,ID:10101010,B=234,Q=345,S=456'
pressure = '4,ID:10101010,BPSS=000,BPSZ=000'

data = pressure
i = 0
while i < 10:
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


