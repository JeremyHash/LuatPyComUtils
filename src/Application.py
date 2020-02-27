from utils import ATestUtils
from domain import ATListFileName
import serial
import sys
import os
import traceback
import multiprocessing
import platform
import signal

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
    sys.exit()
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

diag_pid = 0


def start_trace():
    global diag_pid
    diag_pid = os.getpid()
    print(f'Run diag process {diag_pid}...')
    os.popen(f"./bin/diag trace/log - - /dev/ttyUSB3")


try:
    print(f'Application process {os.getpid()}')
    multiprocessing.Process(target=start_trace).start()
    Application(port, baud_rate, ATListFileNames).run()
except KeyboardInterrupt as ke:
    print()
    print("Exit...")
    os.kill(diag_pid, signal.SIGKILL)
    sys.exit()
except serial.serialutil.SerialException as se:
    print(se)
    os.kill(diag_pid, signal.SIGKILL)
    if ('No such file or directory' in traceback.format_exc()):
        print('输入的端口不存在')
except Exception as e:
    os.kill(diag_pid, signal.SIGKILL)
    print(e)
    print("---------------")
    print(traceback.format_exc())
