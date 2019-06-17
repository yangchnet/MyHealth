from socket import *
import threading
from time import ctime
import pymysql
import datetime
import time

# socket setting
HOST = '::'
POST = 30000
BUFSIZ = 1024
ADDR = (HOST, POST)
tcpSerSock = socket(AF_INET6, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(50)

# mysql setting
db = pymysql.connect(host="localhost", user="ahnu", password="ahnu2019", db="django_mysql", port=3306)
cursor = db.cursor()

def gettime():
    return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%u')

# insert tem
tem = '1,ID:10101010,TEMP=35.45'
def tem_insert(data):
    tm = str(gettime())
    print("time:%s, receive:%s" % (tm,data))
    try:
        data = data[2:]
        dl = data.split(',')
        id = dl[0].split(':')[1]
        tem = dl[1].split('=')[1]
        t = gettime()
        sql = "insert into mhuser_temdata(time, tem_value,own_id, diviceid) values (\'{0}\', \'{1}\', (select user_id from mhuser_normaluser where user_id = (select id from mhuser_mhuser where deviceid=\'{2}\')), \'{2}\')".format(t, tem, id)
        # sql = "insert into mhuser_temdata(time, tem_value,own_id, diviceid) values('2019-03-13 07:07:33.3', '23.23', (select id from mhuser_mhuser where deviceid='10101010'), '10101010')"
        cursor.execute(sql)
        db.commit()
        print('time:%s, data:%s'%(t, data))
        count = threading.active_count()
        print('time:%s, threading: %d' % (t, count))
    except Exception as e:
        print(e)
        return 0

# insert heart
heart = '3,ID=30303030,B=234,Q=345,S=456'
def heart_insert(data):
    tm = str(gettime())
    print("time:%s, receive:%s" % (tm, data))
    try:
        data = data[2:]
        dl = data.split(',')
        id = dl[0].split(':')[1]
        b_value = dl[1].split('=')[1]
        q_value = dl[2].split('=')[1]
        s_value = dl[3].split('=')[1]
        t = gettime()
        sql = "insert into mhuser_heartdata(time, b_value, q_value, s_value, own_id, diviceid) values(\'{0}\', \'{1}\', \'{2}\', \'{3}\', (select user_id from mhuser_normaluser where user_id = (select id from mhuser_mhuser where deviceid=\'{4}\')), \'{4}\')".format(t, b_value, q_value, s_value, id)
        cursor.execute(sql)
        db.commit()
        print('time:%s, data:%s'%(t, data))
        count = threading.active_count()
        print('time:%s, threading: %d' % (t, count))
    except Exception as e:
        print(e)
        return 0

# insert oxygen
oxygen = '2,ID:20202020,HR=123,HRvalid=1,SPO2=321,SPO2valid=1'
def oxygen_insert(data):
    tm = str(gettime())
    print("time:%s, receive:%s" % (tm, data))
    try:
        data = data[2:]
        dl = data.split(',')
        id = dl[0].split(':')[1]
        hr_value = dl[1].split('=')[1]
        hr_v = dl[2].split('=')[1]
        spo2 = dl[3].split('=')[1]
        spo2_v = dl[4].split('=')[1]
        if hr_v == '1' and spo2_v == '1':
            t = gettime()
            sql = "insert into mhuser_oxygendata(time, hr_value, spo2, own_id, diviceid) values(\'{0}\', \'{1}\', \'{2}\', (select user_id from mhuser_normaluser where user_id = (select id from mhuser_mhuser where deviceid=\'{3}\')), \'{3}\')".format(t, hr_value, spo2, id)
            cursor.execute(sql)
            db.commit()
            print('time:%s, data:%s'%(t, data))
            count = threading.active_count()
            print('time:%s, threading: %d' % (t, count))
        else:
            return 0
    except Exception as e:
        print(e)
        return 0

# insert pressure
pressure = '4,ID:40404040,BPSS=345,BPSZ=577'
def pressure_insert(data):
    tm = str(gettime())
    print("time:%s, receive:%s"%(tm, data))
    try:
        data = data[2:]
        dl = data.split(',')
        id = dl[0].split(':')[1]
        bpss = dl[1].split('=')[1]
        bpsz = dl[2].split('=')[1]
        t = gettime()
        sql = "insert into mhuser_pressuredata(time, bpss_value, bpsz_value, own_id, diviceid) values(\'{0}\', \'{1}\', \'{2}\', (select user_id from mhuser_normaluser where user_id = (select id from mhuser_mhuser where deviceid=\'{3}\')), \'{3}\')".format(t, bpss, bpsz, id)
        cursor.execute(sql)
        db.commit()
        print('time:%s, data:%s'%(t, data))
        count = threading.active_count()
        print('time:%s, threading: %d' % (t, count))
    except Exception as e:
        print(e)
        return 0


class Recv(threading.Thread):
    def __init__(self, tcpCliSock):
        super(Recv, self).__init__()
        # print('waiting for connection...')
        # tcpCliSock, addr = tcpSerSock.accept()
        # print('...connected from:', addr)
        self.tcpCliSock = tcpCliSock

    def run(self):
        while True:
            rece_data = self.tcpCliSock.recv(BUFSIZ)
            data = str(rece_data, encoding="utf-8")
            if not rece_data:
                break
            if data[0] == '1':
                send_data = '59.110.140.133'
                self.tcpCliSock.send(send_data.encode())
                tem_insert(data)
            elif data[0] == '2':
                oxygen_insert(data)
            elif data[0] == '3':
                heart_insert(data)
            elif data[0] == '4':
                pressure_insert(data)
            # print(rece_data)
            if rece_data == 'END':
                break
        print("END")


while True:
    t = str(gettime())
    print('time:%s, waiting for connection...'%t)
    count = threading.active_count()
    print('time:%s, threading: %d' % (t,count))
    tcpCliSock, addr = tcpSerSock.accept()
    print('time:%s, ...connected from:%s'%(t, addr))
    # count = threading.current_thread()
    # print(count)

    recv = Recv(tcpCliSock)
    recv.start()
tcpSerSock.close()

