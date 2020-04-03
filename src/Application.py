from utils import ATestUtils
import serial
import sys
import os
import traceback
import multiprocessing
import platform
import signal

# ATListFileNames = ['INIT.txt', 'TCPIP.txt', 'HTTP.txt', 'MQTT.txt', 'FTP.txt']
# ATListFileNames = ['INIT.txt', 'FTP.txt']
# ATListFileNames = ['TMP.txt']
ATListFileNames = ['INIT.txt']
loopTimes = int(input('请输入循环次数：'))
system_cate = platform.system()
print(f'当前操作系统为：{system_cate}')
if system_cate == 'Linux':
    ports = os.popen('python3 -m serial.tools.list_ports').read()
    print(ports)
else:
    ports = os.popen('python -m serial.tools.list_ports').read()
    print(ports)
try:
    while True:
        port = input('请输入测试设备端口号：')
        # port = 'COM74'
        if port not in ports:
            print('输入的端口不存在，请重新输入')
        else:
            break
    while True:
        fileName = input('请输入要测试的功能（FTP,HTTP,MQTT,SMS,TCPIP），输入END结束，全选请输入ALL：')
        if fileName == 'END':
            break
        if fileName == 'ALL':
            ATListFileNames.append('FTP.txt')
            ATListFileNames.append('HTTP.txt')
            ATListFileNames.append('MQTT.txt')
            # ATListFileNames.append('SMS.txt')
            ATListFileNames.append('TCPIP.txt')
            break
        if fileName not in ('FTP', 'HTTP', 'MQTT', 'SMS', 'TCPIP', 'TMP', 'ALL'):
            print('输入的功能名称有误,请重新输入')
            continue
        ATListFileNames.append(f'{fileName}.txt')

    enable_trace = 'n'
    if system_cate == 'Linux':
        enable_trace = input('当前操作系统为Linux，是否抓取trace？（y/n）')
        if enable_trace == 'y':
            diag_port = input('请输入diag诊断口端口：')
except KeyboardInterrupt:
    print()
    print('Exit...')
    sys.exit()
baud_rate = 115200


class Application:

    def __init__(self, port, baud_rate, ATListFileNames, loopTimes):
        self.port = port
        self.baud_rate = baud_rate
        self.ATListFileNames = ATListFileNames
        self.loopTimes = loopTimes

    def run(self):
        app = ATestUtils.ATestUtils(self.port, self.baud_rate)
        app.ATest(self.ATListFileNames, self.loopTimes)


print("JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST")
print("JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST")
print("JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST---JEREMYPYATEST")

diag_pid = 0


def start_trace():
    global diag_pid
    diag_pid = os.getpid()
    print(f'Run diag process {diag_pid}')
    os.popen(f"./bin/diag trace/log - - {diag_port}")


try:
    print(f'Application process {os.getpid()}')
    if system_cate == 'Linux' and enable_trace == 'y':
        multiprocessing.Process(target=start_trace).start()
    Application(port, baud_rate, ATListFileNames, loopTimes).run()
except KeyboardInterrupt as ke:
    print()
    print("Exit...")
    if system_cate == 'Linux' and enable_trace == 'y':
        os.kill(diag_pid, signal.SIGKILL)
    sys.exit()
except serial.serialutil.SerialException as se:
    print(se)
    print("---------------")
    print(traceback.format_exc())
    if system_cate == 'Linux' and enable_trace == 'y':
        os.kill(diag_pid, signal.SIGKILL)
    if 'No such file or directory' in traceback.format_exc():
        print('输入的端口不存在')
    if 'PermissionError' in traceback.format_exc():
        print('端口被占用,请检查是否有其他程序正在占用设备端口')
except Exception as e:
    if system_cate == 'Linux' and enable_trace == 'y':
        os.kill(diag_pid, signal.SIGKILL)
    print(e)
    print("---------------")
    print(traceback.format_exc())
