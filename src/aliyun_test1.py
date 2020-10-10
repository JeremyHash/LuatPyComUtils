import os
import platform
import re
import traceback
import serial
from utils import Logger
import sys
import hmac
import time

# 获取当前系统平台
system_cate = platform.system()
print('当前操作系统为：' + system_cate)
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
    port = 'COM' + input('请指定设备端口号(只需要输入COM后数字):')

product_key = ""
device_name = ""
device_secret = ""


# 阿里云测试类
class aliyun_test:

    # 获取串口操作对象方法
    def serialFactory(self, port, baud_rate):
        return serial.Serial(port=port, baudrate=baud_rate)

    # 构造方法
    def __init__(self, port, baud_rate):
        # 获取log对象
        self.log = Logger.Logger('./log/aliyun_test_log.txt', level='debug')
        # 定义ATList
        self.ATList = []
        # 定义在httppost中发送的内容
        self.post_info = ''
        # 定义测试端口
        self.port = port
        # 定义波特率
        self.baud_rate = baud_rate
        # 获取串口操作对象
        self.ser = self.serialFactory(port, baud_rate)
        # 定义重连次数
        self.frequency = 0
        # 定义DateList
        self.DateList = ""
        self.MusbList = ""

    # 加载ATListFile文件方法
    def load_atList(self, ATListFile):
        with open("./atListFiles/" + ATListFile, encoding="utf8") as file:
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

    # 阿里云测试初始化方法
    def aliyun_init(self):
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

    # 获取mqtt登录信息方法
    def get_mqtt_login_info(self):
        self.ser.timeout = 2
        cmd = f'AT+HTTPDATA={len(self.post_info)},20000\r\n'.encode('GB2312')
        self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
        cmd = self.post_info.encode('GB2312')
        self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
        cmd = b'AT+HTTPACTION=1\r\n'
        self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
        cmd = b'AT+HTTPREAD\r\n'
        self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
        self.ser.write(cmd)
        res = self.ser.read(200).decode(encoding='GB2312')
        self.log.logger.debug(f"收←◆  {res}")
        pattern1 = re.compile(r'"iotId":"\w+"')
        iotId = pattern1.findall(res)[0]
        self.iotId = iotId.replace('"iotId":', '').replace('"', '')
        self.log.logger.debug(f'iotId:{self.iotId}')
        pattern2 = re.compile(r'"iotToken":"[\^\d\w]+"')
        iotToken = pattern2.findall(res)[0]
        self.iotToken = iotToken.replace('"iotToken":', '').replace('"', '')
        self.log.logger.debug(f'iotToken:{self.iotToken}')
        cmd = b'AT+HTTPTERM\r\n'
        self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")

    # 连接阿里云MQTT测试方法
    def connect_mqtt_test(self):
        self.ser.timeout = 1
        cmd = b'1234567890123456789012345678901234567890123456789012345678901234567890'
        self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
        cmd = f'AT+MCONFIG="{device_name}","{self.iotId}","{self.iotToken}"\r\n'.encode('GB2312')
        self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
        self.ser.timeout = 5
        cmd = ('AT+SSLMIPSTART="' + product_key + '.iot-as-mqtt.cn-shanghai.aliyuncs.com",1883\r\n').encode()
        self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
        cmd = b'AT+MCONNECT=1,300\r\n'
        self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
        self.DateList = self.ser.read(200).decode(encoding='GB2312').split("\r\n")
        self.log.logger.debug(self.DateList[4])
        if self.DateList[4] == "CONNECT OK":
            self.log.logger.debug("阿里云MQTT连接成功")
        else:
            self.log.logger.debug("阿里云MQTT连接失败")
        self.ser.timeout = 1
        cmd = ('AT+MSUB="/' + product_key + '/' + device_name + '/user/Jeremy",0\r\n').encode()
        self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
        self.MusbList = self.ser.read(200).decode(encoding='GB2312').split("\r\n")
        self.log.logger.debug(self.MusbList[4])
        if self.MusbList[4] == "SUBACK":
            self.log.logger.debug("订阅成功")
        else:
            self.log.logger.debug("订阅失败,重新订阅")
            cmd = ('AT+MSUB="/' + product_key + '/' + device_name + '/user/Jeremy",0\r\n').encode()
            self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
            self.ser.write(cmd)
            self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
            self.MusbList = self.ser.read(200).decode(encoding='GB2312').split("\r\n")
            self.log.logger.debug(self.MusbList[4])
            if self.MusbList[4] == "SUBACK":
                self.log.logger.debug("订阅成功")
            else:
                self.log.logger.debug("订阅失败，程序退出")
        cmd = b'AT+MQTTMSGSET=0\r\n'
        self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
        startime = int(time.time())
        while True:
            try:
                cmd = ('AT+MPUB="/' + product_key + '/' + device_name + '/user/Jeremy",0,0,"test0"\r\n').encode()
                self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
                self.ser.write(cmd)
                self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
                endtime = int(time.time())
                sub_time = endtime - startime
                self.log.logger.debug("sub_time = " + str(sub_time))
                if sub_time > 300:
                    self.frequency += 1
                    self.log.logger.debug("开始进行第" + str(self.frequency) + "次重启")
                    self.ser.write(b'AT+MIPCLOSE\r\n')
                    self.ser.write(b'AT+MDISCONNECT\r\n')
                    self.ser.write(b'AT+RESET\r\n')
                    self.ser.close()
                    for waitime in range(10):
                        self.log.logger.debug("正在重启中，请等待。。。")
                        time.sleep(3)
                    self.ser.open()
                    self.log.logger.debug("第" + str(self.frequency) + "次重启成功")
                    self.log.logger.debug("开始连接阿里云MQTT")
                    self.connect_mqtt_test()
            except UnicodeError as e:
                self.log.logger.error(e)
                self.log.logger.error("---------------解码异常---------------")
                self.log.logger.error(traceback.format_exc())


def AlicloudMachineTest():
    global device_name, product_key, device_secret
    test = aliyun_test(port, 115200)
    # # 一机一密测试
    test.load_atList('INIT.txt')
    test.load_atList('ALIYUN一机一密.txt')
    test.aliyun_init()
    with open('./cfg/one_device_one_secret.txt') as f:
        lines = f.readlines()
        product_key = lines[0].replace('\n', '')
        device_name = lines[1].replace('\n', '')
        device_secret = lines[2].replace('\n', '')
    test.log.logger.debug(f'ProductKey:{product_key}')
    test.log.logger.debug(f'DeviceName:{device_name}')
    test.log.logger.debug(f'DeviceSecret:{device_secret}')
    # 拼接加密前明文
    message = b'clientId' + device_name.encode('GB2312') + b'deviceName' + device_name.encode(
        'GB2312') + b'productKey' + product_key.encode('GB2312')
    key = device_secret.encode('GB2312')
    # 使用HMACMD5算法用设备密钥加密明文
    sign = hmac.new(key, message, digestmod='MD5')
    # 拼接http_post发送信息
    test.post_info = f'productKey={product_key}&sign={sign.hexdigest()}&clientId={device_name}&deviceName={device_name}'
    test.get_mqtt_login_info()
    test.connect_mqtt_test()


try:
    AlicloudMachineTest()
except KeyboardInterrupt as ke:
    print("exit...")
    sys.exit(0)
except Exception as e:
    print(e)
    print("---------------")
    print(traceback.format_exc())
