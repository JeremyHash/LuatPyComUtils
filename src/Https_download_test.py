import os
import platform
import traceback

import serial
from utils import Logger
import sys

system_cate = platform.system()
print(f'当前操作系统为：{system_cate}')
if system_cate == 'Linux':
    ports = os.popen('python3 -m serial.tools.list_ports').read()
    print(ports)
else:
    ports = os.popen('python -m serial.tools.list_ports').read()
    print(ports)
port = input('请指定设备端口号:')


class Https_download_test:
    log = Logger.Logger('./log/http_download_log.txt', level='debug')
    tmp_ATListFileNames = ['HTTP_DOWNLOAD.TXT']
    ATList = []

    def serialFactory(self, port, baud_rate):
        return serial.Serial(port=port, baudrate=baud_rate)

    def print_hex(bytes_data):
        l = [hex(int(i)) for i in bytes_data]
        print(" ".join(l))

    def __init__(self, port, baud_rate):
        self.port = port
        self.baud_rate = baud_rate
        self.ser = self.serialFactory(port, baud_rate)

    def loadATList(self):
        for ATListFile in self.tmp_ATListFileNames:
            with open("./atListFiles/" + ATListFile, encoding="UTF8") as file:
                print()
                print(f"【正在加载的ATListFileName：】{ATListFile}")
                print()
                lines = file.readlines()
                tmp_count = 0
                for line in lines:
                    if not line.startswith("#"):
                        if not line.isspace():
                            cmd_contents = line.replace("\n", "").split("====")
                            print(f"ATCmd:{cmd_contents[0]}")
                            self.ATList.append(cmd_contents)
                            tmp_count += 1
            print()
            print(f"【成功加载---{ATListFile}---ATCmd{str(tmp_count)}条】")
            print()

    def ATest(self):
        if self.ser.is_open:
            if len(self.ATList) == 0:
                print("ATList为空")
                sys.exit(0)
            for ATCmd in self.ATList:
                self.ser.timeout = int(ATCmd[2])
                tmp1 = (ATCmd[0] + "\r\n").encode("UTF8")
                self.ser.write(tmp1)
                self.log.logger.debug(f"发→◇  {ATCmd[0]}")
                res = self.ser.read(1000)
                tmp2 = res.decode(encoding="UTF8")
                self.log.logger.debug(f"收←◆  {tmp2}")
        else:
            print(f"{self.ser.port}端口打开失败")

    def setbreak(self):
        i = 0
        j = 9999
        while True:
            self.ser.timeout = 1
            cmd = b'AT+HTTPPARA=BREAK,%d\r\n' % i
            self.log.logger.debug(f"发→◇  {cmd.decode()}")
            self.ser.write(cmd)
            self.log.logger.debug(f"收←◆  {self.ser.read(2000).decode()}")
            cmd = b'AT+HTTPPARA=BREAKEND,%d\r\n' % j
            self.log.logger.debug(f"发→◇  {cmd.decode()}")
            self.ser.write(cmd)
            self.log.logger.debug(f"收←◆  {self.ser.read(2000).decode()}")
            self.ser.timeout = 5
            cmd = b'AT+HTTPACTION=0\r\n'
            self.log.logger.debug(f"发→◇  {cmd.decode()}")
            self.ser.write(cmd)
            temp = self.ser.read(2000).decode()
            self.log.logger.debug(f"收←◆  {temp}")
            if "416" in temp:
                break
            cmd = b'AT+HTTPREAD\r\n'
            self.log.logger.debug(f"发→◇  {cmd.decode()}")
            self.ser.write(cmd)
            self.log.logger.debug(f"收←◆  ")
            self.log.logger.debug(self.ser.read(20000))
            print()
            i += 10000
            j += 10000
        # self.ser.close()


try:
    test = Https_download_test(port, 115200)
    test.loadATList()
    test.ATest()
    count = 1
    while True:
        test.setbreak()
        test.log.logger.debug(f'第{count}次http下载测试完成。。。')
        count = count + 1
except KeyboardInterrupt as ke:
    print("exit...")
    sys.exit()
except Exception as e:
    print(e)
    print("---------------")
    print(traceback.format_exc())
