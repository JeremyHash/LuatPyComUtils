import os
import platform
import re
import traceback
import serial
from utils import Logger
import sys
import hmac

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

# 请求输入测试端口
port = input('请指定设备测试端口号:')


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

    # 获取设备密钥方法
    def get_device_secret(self):
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
        pattern = re.compile(r'"deviceSecret":"\w+"')
        device_secret = pattern.findall(res)[0]
        self.device_secret = device_secret.replace('"deviceSecret":', '').replace('"', '')
        self.log.logger.debug(f'deviceSecret:{self.device_secret}')
        cmd = b'AT+HTTPTERM\r\n'
        self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")

    # 连接阿里云MQTT测试方法
    def connect_mqtt_test(self):
        self.ser.timeout = 1
        cmd = f'AT+MCONFIG="{device_name}","{self.iotId}","{self.iotToken}"\r\n'.encode('GB2312')
        self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
        # cmd = b'AT+CDNSCFG="114.114.114.114","114.114.114.114",1\r\n'
        # self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
        # self.ser.write(cmd)
        # self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
        self.ser.timeout = 5
        cmd = ('AT+SSLMIPSTART="' + product_key + '.iot-as-mqtt.cn-shanghai.aliyuncs.com",1883\r\n').encode()
        self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
        cmd = b'AT+MCONNECT=1,300\r\n'
        self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
        self.ser.timeout = 1
        cmd = ('AT+MSUB="/' + product_key + '/' + device_name + '/user/Jeremy",0\r\n').encode()
        self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
        cmd = b'AT+MQTTMSGSET=0\r\n'
        self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
        while True:
            try:
                cmd = ('AT+MPUB="/' + product_key + '/' + device_name + '/user/Jeremy",0,0,"test0"\r\n').encode()
                self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
                self.ser.write(cmd)
                self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
                cmd = ('AT+MPUB="/' + product_key + '/' + device_name + '/user/Jeremy",1,0,"test1"\r\n').encode()
                self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
                self.ser.write(cmd)
                self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
            except UnicodeError as e:
                self.log.logger.error(e)
                self.log.logger.error("---------------解码异常---------------")
                self.log.logger.error(traceback.format_exc())


if __name__ == '__main__':
    try:
        test = aliyun_test(port, 115200)
        test_type = input('''阿里云测试项：1.一机一密 2.一型一密 
您要进行的测试是:''')
        # 一机一密测试
        if test_type == '1':
            test.load_atList('INIT.txt')
            test.load_atList('ALIYUN一机一密.txt')
            print('开始执行命令,log见./log/aliyun_test_log.txt')
            test.aliyun_init()
            # 读取一机一密配置文件
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
        # 一型一密测试
        elif test_type == '2':
            test.load_atList('INIT.txt')
            test.load_atList('ALIYUN一型一密_getDeviceSecret.txt')
            test.aliyun_init()
            with open('./cfg/one_product_one_secret.txt') as f:
                lines = f.readlines()
            product_key = lines[0].replace('\n', '')
            device_name = lines[1].replace('\n', '')
            product_secret = lines[2].replace('\n', '')
            test.log.logger.debug(f'ProductKey:{product_key}')
            test.log.logger.debug(f'DeviceName:{device_name}')
            test.log.logger.debug(f'ProductSecret:{product_secret}')
            # 拼接明文
            message = f'deviceName{device_name}productKey{product_key}random123456'.encode()
            key = product_secret.encode('GB2312')
            # 使用HMACMD5算法用设备密钥加密明文
            sign = hmac.new(key, message, digestmod='MD5')
            # 拼接http_post发送信息
            test.post_info = f'productKey={product_key}&deviceName={device_name}&random=123456&sign={sign.hexdigest()}&signMethod=HmacMD5'
            # 获取设备密钥
            test.get_device_secret()
            # 拼接明文
            message = f'clientId{device_name}deviceName{device_name}productKey{product_key}'.encode()
            key = test.device_secret.encode('GB2312')
            # 使用HMACMD5算法用设备密钥加密明文
            sign = hmac.new(key, message, digestmod='MD5')
            # 拼接http_post发送信息
            test.post_info = f'productKey={product_key}&sign={sign.hexdigest()}&clientId={device_name}&deviceName={device_name}'
            # 清空ATList列表
            test.ATList = []
            # 加载获取MQTT登录信息的ATCmd
            test.load_atList('ALIYUN一型一密_getMQTTLoginInfo.txt')
            test.aliyun_init()
            test.get_mqtt_login_info()
            test.connect_mqtt_test()
        else:
            print('输入有误')
            sys.exit(0)

    except KeyboardInterrupt as ke:
        print("exit...")
        sys.exit()
    except Exception as e:
        print(e)
        print("---------------")
        print(traceback.format_exc())
