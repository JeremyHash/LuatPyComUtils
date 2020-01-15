# import serial
#
# ser = serial.Serial(port="com4",timeout=1)
# print(ser)
# ser.write(b'AT\r\n')
# res = ser.read(100)
# print(res)
# ser.close()

# with serial.Serial(port="COM4",timeout=2,baudrate=115200) as ser:
#     ser.write(b'AT\r\n')
#     x = ser.read(100)
#     print(x)
# import time
#
# for i in range(5):
#     print(i)
#     time.sleep(2)
import functools

# def log(text):
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             print('%s %s():' % (text, func.__name__))
#             return func(*args, **kwargs)
#
#         return wrapper
#
#     return decorator
#
#
# @log('execute')

# print(now.__name__)

# def log(func):
#     @functools.wraps(func)
#     def wrapper(*args, **kwargs):
#         print('call %s()' % func.__name__)
#         return func(*args, **kwargs)
#
#     return wrapper
#
#
# @log
# def now():
#     print('2020-1-14')
#
#
# now()

# import socket
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect(("www.baidu.com", 80))
# s.send(b'GET / HTTP/1.1\r\nHost: www.baidu.com\r\nConnection: close\r\n\r\n')
# buffer = []
# while True:
#     d = s.recv(1024)
#     if d:
#         buffer.append(d)
#     else:
#         break
# data = b''.join(buffer)
# header, html = data.split(b'\r\n\r\n', 1)
# print(header.decode('utf-8'))
# print(html.decode('utf8'))
# s.close()

import socket
import threading
import time


def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcome!')
    while True:
        data = sock.recv(1024)
        time.sleep(1)
        if not data or data.decode('utf-8') == 'exit':
            break
        sock.send(('Hello, %s!' % data.decode('utf-8')).encode('utf-8'))
    sock.close()
    print('Connection from %s:%s closed.' % addr)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 9999))
s.listen(5)
print("等待连接。。。")
while True:
    sock, addr = s.accept()
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
