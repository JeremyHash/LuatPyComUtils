import serial
from utils import Logger
import sys


class https_download_test:
    # log = Logger.Logger('./log/log.txt', level='debug')

    def serialFactory(self, port, baud_rate):
        return serial.Serial(port=port, baudrate=baud_rate)

    def print_hex(bytes_data):
        l = [hex(int(i)) for i in bytes_data]
        print(" ".join(l))

    def __init__(self, port, baud_rate):
        self.ser = self.serialFactory(port, baud_rate)

    def ATest(self):
        if self.ser.is_open:
            self.ser.timeout = 2
            # self.ser.write(b'ATE0"\r\n')
            self.ser.write(b'AT+SAPBR=3,1,"Contype","GPRS"\r\n')
            res = self.ser.read(1000)
            print(res)
            self.ser.close()
            # while True:
        # for ATCmd in self.ATList:
        # tmp1 = (ATCmd[0] + "\r\n").encode("UTF8")
        # self.ser.write(tmp1)
        # self.log.logger.debug("【发送AT】:" + ATCmd[0])
        # res = self.ser.read(1000)
        # tmp2 = res.decode(encoding="UTF8")
        # self.log.logger.debug("【串口返回】:" + tmp2)
        # if ATCmd[1] in tmp2:
        #     self.log.logger.debug("命令【" + ATCmd[0] + "】匹配成功")
        # else:
        #     self.log.logger.warning("命令【" + ATCmd[0] + "】匹配失败")
        else:
            print(self.ser.port, "端口打开失败")


https_download_test('COM8', 115200).ATest()
