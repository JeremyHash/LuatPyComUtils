import re
import traceback

import serial
from utils import Logger, utils
import sys


# ATestUtils类
class ATestUtils:
    # 统计匹配出错次数
    error_count = 0
    # ATList列表
    ATList = []
    # 获取log对象,log位置为./log/log.txt log等级为debug
    log = Logger.Logger('./log/log.txt', level='debug')

    # 串口对象生成Factory
    def serialFactory(self, port, baud_rate):
        return serial.Serial(port=port, baudrate=baud_rate)

    # 构造方法生成串口操作对象
    def __init__(self, port, baud_rate):
        self.ser = self.serialFactory(port, baud_rate)

    # 加载ATlist方法
    def loadATList(self, ATListFileNames):
        # 用来记录总加载ATCmd数量
        sum_AT_count = 0
        # 遍历传入的ATListFileNames
        for ATListFile in ATListFileNames:
            # 读取对应的ATList文件
            with open("./atListFiles/" + ATListFile, encoding="UTF8") as file:
                print()
                print(f"【正在加载的ATListFileName：】{ATListFile}")
                print()
                # 读出文件中的所有行储存在列表中
                lines = file.readlines()
                # 用来记录加载的ATCmd数量
                ATCmdCount = 0
                # 遍历读出的所有行
                for line in lines:
                    # 如果开头没有注释标记井号且不为空行，则为有效ATCmd
                    if not line.startswith("#"):
                        if not line.isspace():
                            # 去除结尾换行\n，然后用四个等于号作为分割方式切分这一行内容
                            cmd_contents = line.replace("\n", "").split("====")
                            # 打印获取到的ATCmd
                            print(f"ATCmd:{cmd_contents[0]}")
                            # 将分割结果存入ATList列表
                            self.ATList.append(cmd_contents)
                            ATCmdCount += 1
                            sum_AT_count += 1
            print()
            print(f"【成功加载---{ATListFile}---ATCmd{ATCmdCount}条】")
            print()
        print(f'成功加载ATCmd共{sum_AT_count}条')

    # ATest方法，循环发送ATCmd，读取结果，校验格式
    def ATest(self, ATListFileNames, loopTimes):
        global tmp2
        # 如果串口对象处于可操作状态
        if self.ser.is_open:
            # 加载ATlistFileNames
            self.loadATList(ATListFileNames)
            # 如果加载之后ATList为空，说明没有添加任何测试项目，退出程序
            if len(self.ATList) == 0:
                print("ATList为空")
                sys.exit(0)
            # while True:
            print('开始执行命令,log见./log/log.txt')
            # 循环控制台输入的指定次数
            for i in range(loopTimes):
                print(f'第{i + 1}次循环开始')
                # 循环执行ATList中的ATCmd
                for ATCmd in self.ATList:
                    # 设置串口对象读取延时
                    self.ser.timeout = int(ATCmd[2])
                    tmp1 = (ATCmd[0] + "\r\n").encode("GB2312")
                    # 将文件中本来是\n或\r的内容因为读取到程序中变为\\n \\r 的部分替换回去
                    tmp1 = tmp1.replace(b"\\n", b"\n")
                    tmp1 = tmp1.replace(b"\\r", b"\r")
                    # 串口对象向对应串口发送数据
                    self.ser.write(tmp1)
                    self.log.logger.debug(f"发→◇  {ATCmd[0]}")
                    # 读取串口返回内容，读取的字节数尽量大一点，因为后面http相关的命令会返回非常大的数据
                    res = self.ser.read(320000)
                    # 由于http部分返回的某些数据无法正常解码，所以在这里抓取这个异常
                    try:
                        tmp2 = res.decode(encoding='GB2312')
                    except UnicodeDecodeError as ude:
                        print('解码异常')
                        print(ude)
                        print("---------------")
                        print(traceback.format_exc())
                    self.log.logger.debug(f"收←◆  {tmp2}")
                    # 打印接收到的数据的十六进制
                    hexdata = '收←◆  hex_data: ' + utils.get_hex(res)
                    self.log.logger.debug(hexdata)
                    # 用配置文件中写好的正则规则去匹配返回的结果
                    try:
                        if re.match(ATCmd[1], tmp2):
                            self.log.logger.debug("命令【" + ATCmd[0] + "】匹配成功")
                        else:
                            self.log.logger.warning("命令【" + ATCmd[0] + "】匹配失败")
                            # 记录匹配失败的次数
                            self.error_count = self.error_count + 1
                    except Exception as e:
                        print(e)
                        self.log.logger.warning("命令【" + ATCmd[0] + "】匹配异常")
                        print(traceback.format_exc())
                print(f'第{i + 1}次循环完成')
        else:
            print(f"{self.ser.port}端口打开失败")
