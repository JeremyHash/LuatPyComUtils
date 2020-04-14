import serial
from utils import Logger
import sys
import re


class ATestUtils:
    ATList = []
    log = Logger.Logger('./log/log.txt', level='debug')

    def serialFactory(self, port, baud_rate):
        return serial.Serial(port=port, baudrate=baud_rate)

    def print_hex(self, bytes_data):
        l = [hex(int(i)) for i in bytes_data]
        print(" ".join(l))

    def __init__(self, port, baud_rate):
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

    def ATest(self, ATListFileNames, loopTimes):
        self.tmp_ATListFileNames = ATListFileNames
        if self.ser.is_open:
            self.loadATList()
            if len(self.ATList) == 0:
                print("ATList为空")
                sys.exit(0)
            # while True:
            for i in range(loopTimes):
                for ATCmd in self.ATList:
                    self.ser.timeout = int(ATCmd[2])
                    tmp1 = (ATCmd[0] + "\r\n").encode("UTF8")
                    self.ser.write(tmp1)
                    self.log.logger.debug(f"发→◇  {ATCmd[0]}")
                    res = self.ser.read(210000)
                    tmp2 = res.decode(encoding="UTF8")
                    self.log.logger.debug(f"收←◆  {tmp2}")
                    try:
                        # if re.match(ATCmd[1], tmp2.replace('\r\n', '')):
                        if re.match(ATCmd[1], tmp2):
                            self.log.logger.debug("命令【" + ATCmd[0] + "】匹配成功")
                        else:
                            self.log.logger.warning("命令【" + ATCmd[0] + "】匹配失败")
                    except Exception:
                        print("匹配异常")
                        pass
        else:
            print(f"{self.ser.port}端口打开失败")
