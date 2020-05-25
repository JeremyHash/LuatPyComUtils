import os
import platform
import re
import traceback
import serial
from utils import Logger
import sys
import hmac

system_cate = platform.system()
print(f'当前操作系统为：{system_cate}')
if system_cate == 'Linux':
    ports = os.popen('python3 -m serial.tools.list_ports').read()
    print(ports)
else:
    ports = os.popen('python -m serial.tools.list_ports').read()
    print(ports)
port = input('请指定设备测试端口号:')


class aliyun_test:

    def serialFactory(self, port, baud_rate):
        return serial.Serial(port=port, baudrate=baud_rate)

    def __init__(self, port, baud_rate):
        self.log = Logger.Logger('./log/aliyun_test.log', level='debug')
        self.ATList = []
        self.post_info = ''
        self.port = port
        self.baud_rate = baud_rate
        self.ser = self.serialFactory(port, baud_rate)

    def load_atList(self, ATListFile):
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

    def aliyun_init(self):
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

    def get_mqtt_login_info(self):
        self.ser.timeout = 2
        cmd = f'AT+HTTPDATA={len(self.post_info)},20000\r\n'.encode('utf8')
        self.log.logger.debug(f"发→◇  {cmd.decode()}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode()}")
        cmd = self.post_info.encode('utf8')
        self.log.logger.debug(f"发→◇  {cmd.decode()}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode()}")
        cmd = b'AT+HTTPACTION=1\r\n'
        self.log.logger.debug(f"发→◇  {cmd.decode()}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode()}")
        cmd = b'AT+HTTPREAD\r\n'
        self.log.logger.debug(f"发→◇  {cmd.decode()}")
        self.ser.write(cmd)
        res = self.ser.read(200).decode()
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
        self.log.logger.debug(f"发→◇  {cmd.decode()}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode()}")

    def get_device_secret(self):
        self.ser.timeout = 2
        cmd = f'AT+HTTPDATA={len(self.post_info)},20000\r\n'.encode('utf8')
        self.log.logger.debug(f"发→◇  {cmd.decode()}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode()}")
        cmd = self.post_info.encode('utf8')
        self.log.logger.debug(f"发→◇  {cmd.decode()}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode()}")
        cmd = b'AT+HTTPACTION=1\r\n'
        self.log.logger.debug(f"发→◇  {cmd.decode()}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode()}")
        cmd = b'AT+HTTPREAD\r\n'
        self.log.logger.debug(f"发→◇  {cmd.decode()}")
        self.ser.write(cmd)
        res = self.ser.read(200).decode()
        self.log.logger.debug(f"收←◆  {res}")
        pattern = re.compile(r'"deviceSecret":"\w+"')
        device_secret = pattern.findall(res)[0]
        self.device_secret = device_secret.replace('"deviceSecret":', '').replace('"', '')
        self.log.logger.debug(f'deviceSecret:{self.device_secret}')
        cmd = b'AT+HTTPTERM\r\n'
        self.log.logger.debug(f"发→◇  {cmd.decode()}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode()}")

    def connect_mqtt_test(self):
        self.ser.timeout = 1
        cmd = f'AT+MCONFIG="{device_name}","{self.iotId}","{self.iotToken}"\r\n'.encode('utf8')
        self.log.logger.debug(f"发→◇  {cmd.decode()}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode()}")
        # cmd = b'AT+CDNSCFG="114.114.114.114","114.114.114.114",1\r\n'
        # self.log.logger.debug(f"发→◇  {cmd.decode()}")
        # self.ser.write(cmd)
        # self.log.logger.debug(f"收←◆  {self.ser.read(200).decode()}")
        self.ser.timeout = 5
        cmd = ('AT+SSLMIPSTART="' + product_key + '.iot-as-mqtt.cn-shanghai.aliyuncs.com",1883\r\n').encode()
        self.log.logger.debug(f"发→◇  {cmd.decode()}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode()}")
        cmd = b'AT+MCONNECT=1,300\r\n'
        self.log.logger.debug(f"发→◇  {cmd.decode()}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode()}")
        self.ser.timeout = 2
        cmd = ('AT+MSUB="/' + product_key + '/' + device_name + '/user/Jeremy",0\r\n').encode()
        self.log.logger.debug(f"发→◇  {cmd.decode()}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode()}")
        cmd = b'AT+MQTTMSGSET=0\r\n'
        self.log.logger.debug(f"发→◇  {cmd.decode()}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode()}")
        while True:
            cmd = ('AT+MPUB="/' + product_key + '/' + device_name + '/user/Jeremy",0,0,"test0"\r\n').encode()
            self.log.logger.debug(f"发→◇  {cmd.decode()}")
            self.ser.write(cmd)
            self.log.logger.debug(f"收←◆  {self.ser.read(200).decode()}")
            cmd = ('AT+MPUB="/' + product_key + '/' + device_name + '/user/Jeremy",1,0,"test1"\r\n').encode()
            self.log.logger.debug(f"发→◇  {cmd.decode()}")
            self.ser.write(cmd)
            self.log.logger.debug(f"收←◆  {self.ser.read(200).decode()}")


if __name__ == '__main__':
    try:
        test = aliyun_test(port, 115200)
        test_type = input('''阿里云测试项：1.一机一密 2.一型一密 
您要进行的测试是:''')
        if test_type == '1':
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
            message = b'clientId' + device_name.encode('utf8') + b'deviceName' + device_name.encode(
                'utf8') + b'productKey' + product_key.encode('utf8')
            key = device_secret.encode('utf8')
            sign = hmac.new(key, message, digestmod='MD5')
            test.post_info = f'productKey={product_key}&sign={sign.hexdigest()}&clientId={device_name}&deviceName={device_name}'
            test.get_mqtt_login_info()
            test.connect_mqtt_test()
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
            message = f'deviceName{device_name}productKey{product_key}random123456'.encode()
            key = product_secret.encode('utf8')
            sign = hmac.new(key, message, digestmod='MD5')
            test.post_info = f'productKey={product_key}&deviceName={device_name}&random=123456&sign={sign.hexdigest()}&signMethod=HmacMD5'
            test.get_device_secret()
            message = f'clientId{device_name}deviceName{device_name}productKey{product_key}'.encode()
            key = test.device_secret.encode('utf8')
            sign = hmac.new(key, message, digestmod='MD5')
            test.post_info = f'productKey={product_key}&sign={sign.hexdigest()}&clientId={device_name}&deviceName={device_name}'
            test.ATList = []
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
