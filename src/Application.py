from utils import ATestUtils
from domain import ATListFileName
import serial
import os
import traceback
import platform

system_cate = platform.system()
print(f'当前操作系统为：{system_cate}')
if system_cate == 'Linux':
    ports = os.popen('python3 -m serial.tools.list_ports').read()
    print(ports)
try:
    port = input('请输入测试设备端口号：')
except KeyboardInterrupt:
    print()
    print('Exit...')
baud_rate = 115200
ATListFileNames = [ATListFileName.INIT, ATListFileName.TMP, ]


class Application:

    def __init__(self, port, baud_rate, ATListFileNames):
        self.port = port
        self.baud_rate = baud_rate
        self.ATListFileNames = ATListFileNames

    def run(self):
        app = ATestUtils.ATestUtils(self.port, self.baud_rate)
        app.ATest(self.ATListFileNames)


print("JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST")
print("JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST")
print("JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST")
try:
    Application(port, baud_rate, ATListFileNames).run()
except KeyboardInterrupt as ke:
    print()
    print("Exit...")
except serial.serialutil.SerialException as se:
    print(se)
    if ('No such file or directory' in traceback.format_exc()):
        print('输入的端口不存在')
except Exception as e:
    print(e)
    print("---------------")
    print(traceback.format_exc())
