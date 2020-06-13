import os
import time

# 请求用户输入要循环开关闭的网卡名称
eth_name = input('请输入要循环启用关闭的网卡名称：')
# 记录循环次数
i = 1
while True:
    # 关闭指定网卡
    os.popen('ifconfig ' + eth_name + ' down')
    print(eth_name + '网卡关闭了')
    # 休眠5S
    time.sleep(5)
    # 开启指定网卡
    os.popen('ifconfig ' + eth_name + ' up')
    print(eth_name + '网卡开启了')
    # 休眠5S
    time.sleep(5)
    print('第' + str(i) + '次循环结束')
    i = i + 1
