import os
import platform
import traceback

import serial
from utils import Logger
import sys

# 查询系统平台
system_cate = platform.system()
print(f'当前操作系统为：{system_cate}')

# 显示当前所有端口（在Linux下使用python要指明python3）
if system_cate == 'Linux':
    ports = os.popen('python3 -m serial.tools.list_ports').read()
    print(ports)
# macOS系统平台为Darwin
elif system_cate == 'Darwin':
    ports = os.popen('python3 -m serial.tools.list_ports').read()
    print(ports)
else:
    ports = os.popen('python -m serial.tools.list_ports').read()
    print(ports)
# 如果没有查询到端口，则提示用户需要连接模块
if "" == ports:
    print("没有检测到端口，请连接模块")
    sys.exit(0)
port = input('请指定设备端口号:')


# http断点下载测试
class Https_download_test:
    log = Logger.Logger('./log/http_download_log.txt', level='debug')
    tmp_ATListFileNames = ['HTTP_DOWNLOAD.txt']
    ATList = []

    # 生成串口操作对象
    def serialFactory(self, port, baud_rate):
        return serial.Serial(port=port, baudrate=baud_rate)

    # 构造方法
    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = self.serialFactory(port, baud_rate)

    # 加载ATList
    def loadATList(self):
        for ATListFile in self.tmp_ATListFileNames:
            with open("./atListFiles/" + ATListFile, encoding="UTF8") as file:
                print()
                print("【正在加载的ATListFileName：】" + ATListFile)
                print()
                lines = file.readlines()
                tmp_count = 0
                for line in lines:
                    if not line.startswith("#"):
                        if not line.isspace():
                            cmd_contents = line.replace("\n", "").split("====")
                            print("ATCmd:" + cmd_contents[0])
                            self.ATList.append(cmd_contents)
                            tmp_count += 1
            print()
            print("【成功加载---" + ATListFile + "---ATCmd" + str(tmp_count) + "条】")
            print()

    # ATest方法
    def ATest(self):
        if self.ser.is_open:
            if len(self.ATList) == 0:
                print("ATList为空")
                sys.exit(0)
            for ATCmd in self.ATList:
                self.ser.timeout = float(ATCmd[2])
                tmp1 = (ATCmd[0] + "\r\n").encode("GB2312")
                self.ser.write(tmp1)
                self.log.logger.debug(f"发→◇  {ATCmd[0]}")
                res = self.ser.read(1000)
                tmp2 = res.decode(encoding="GB2312")
                self.log.logger.debug(f"收←◆  {tmp2}")
        else:
            print(self.ser.port + "端口打开失败")

    # 循环设置断点
    def setbreak(self):
        start = 0
        end = 59999
        i = start
        j = end
        while True:
            self.ser.timeout = 1
            cmd = b'AT+HTTPPARA=BREAK,%d\r\n' % i
            self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
            self.ser.write(cmd)
            self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
            cmd = b'AT+HTTPPARA=BREAKEND,%d\r\n' % j
            self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
            self.ser.write(cmd)
            self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
            self.ser.timeout = 5
            cmd = b'AT+HTTPACTION=0\r\n'
            self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
            self.ser.write(cmd)
            temp = self.ser.read(200).decode(encoding='GB2312')
            self.log.logger.debug(f"收←◆  {temp}")
            self.ser.timeout = 10
            cmd = b'AT+HTTPREAD\r\n'
            self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
            self.ser.write(cmd)
            self.log.logger.debug(f"收←◆  ")
            self.log.logger.debug(self.ser.read(200000))
            if str(end + 1) not in temp:
                break
            i += end + 1
            j += end + 1
        # self.ser.close()


try:
    test = Https_download_test(port, 115200)
    test.loadATList()
    test.ATest()
    count = 1
    while True:
        test.setbreak()
        test.log.logger.debug('第' + count + '次http下载测试完成。。。')
        count = count + 1
except KeyboardInterrupt as ke:
    print("exit...")
    sys.exit()
except Exception as e:
    print(e)
    print("---------------")
    print(traceback.format_exc())
