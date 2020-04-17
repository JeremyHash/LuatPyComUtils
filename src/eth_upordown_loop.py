import os
import time

eth_name = input('请输入要循环启用关闭的网卡名称：')
i = 1
while True:
    os.popen('ifconfig ' + eth_name + ' down')
    print(eth_name + '网卡关闭了')
    time.sleep(5)
    os.popen('ifconfig ' + eth_name + ' up')
    print(eth_name + '网卡开启了')
    time.sleep(5)
    print('第' + i + '次循环结束')
    i = i + 1
