import os
import serial
import time

ports = os.popen('python -m serial.tools.list_ports').read()
port = ports.split()
print(port)
port = port[1]
print(port)
# 初始化波特率设置
baud_rate = 115200
# 向模块发送数据
ser = serial.Serial(port, baud_rate)
ser.timeout = 2
data = []


def settype():
    ser.write(b'AT+CPBS=SM\r\n')
    ser.write(b'AT+CPBS?\r\n')
    res = ser.read(100)
    res = data.append(res.decode(encoding="GB2312"))


def writeple():
    for i in data:
        j = i.split('\r\n')
        print(j)
        # 1802
        k = j[5].split(',')
        # 1802s
        # k = j[3].split(',')
        # 8910
        # k = j[2].split(',')
        n = k[2]
        if int(n) == 50:
            for m in range(1, 51, 1):
                # 删除电话号码
                # strlist = 'AT+CPBW=' + str(m)
                # 拼接电话号码
                strlist = 'AT+CPBW=' + str(m) + ',15012345678' + ',129,' + str(m) + '_zhangsan'
                serstr = (strlist + "\r\n").encode("GB2312")
                print(serstr)
                # 添加电话号码
                ser.write(serstr)
        elif int(n) == 500:
            for m in range(1, 501, 1):
                strlist = 'AT+CPBW=' + str(m)
                # strlist = 'AT+CPBW=' + str(m) + ',15012345678' + ',129,' + str(m) + '_zhangsan'
                serstr = (strlist + "\r\n").encode("GB2312")
                print(serstr)
                ser.write(serstr)
                time.sleep(0.1)
        else:
            pass


if __name__ == '__main__':
    settype()
    writeple()
