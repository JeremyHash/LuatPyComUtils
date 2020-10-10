from utils import ATestUtils
import serial
import sys
import os
import traceback
import multiprocessing
import platform
import signal


# Application类
class Application:

    # 构造方法
    def __init__(self, port, baud_rate, ATListFileNames, loopTimes):
        self.port = port
        self.baud_rate = baud_rate
        self.ATListFileNames = ATListFileNames
        self.loopTimes = loopTimes

    # 程序运行方法
    def run(self):
        app = ATestUtils.ATestUtils(self.port, self.baud_rate)
        app.ATest(self.ATListFileNames, self.loopTimes)
        print('共匹配失败' + str(app.error_count) + '次')


# 定义ATListFiles，用来储存要运行的ATList文件列表
ATListFileNames = []
# 初始化串口波特率设置
baud_rate = 115200
# trace控制选项，n为关闭，y为打开
enable_trace = 'n'
# 诊断进程pid
diag_pid = 0
# 查询系统平台
system_cate = platform.system()
print('当前操作系统为：' + system_cate)

try:
    # 如果控制台传入的参数数量为2且第二个参数为-h,则显示运行帮助
    if len(sys.argv) == 2 and sys.argv[1] == '-h':
        print('''   useage: 
            Linux: nohup python3 Application {port} {loopTimes}&!
            Windows: python Application {port} {loopTimes}''')
        sys.exit(0)

    # 如果控制台传入的参数数量为1，则说明没有用户自定义参数，此时询问用户输入必要信息，串口，循环次数，测试功能
    elif len(sys.argv) == 1:
        # 请求输入循环次数
        loopTimes = int(input('请输入循环次数：'))

        # 显示当前所有端口（在Linux下使用python要指明python3）
        if system_cate == 'Linux':
            ports = os.popen('python3 -m serial.tools.list_ports').read()
            print(ports)
            port = '/dev/ttyUSB' + input('请指定设备端口号(只需要输入/dev/ttyUSB后数字):')
        # macOS系统平台为Darwin
        elif system_cate == 'Darwin':
            ports = os.popen('python3 -m serial.tools.list_ports').read()
            print(ports)
            port = input('请指定设备端口号:')
        else:
            ports = os.popen('python -m serial.tools.list_ports').read()
            print(ports)
            port = 'COM' + input('请指定设备端口号(只需要输入COM后数字):')
        # 如果没有查询到端口，则提示用户需要连接模块
        if "" == ports:
            print("没有检测到端口，请连接模块")
            sys.exit(0)

        # 请求输入测试功能
        while True:
            fileName = input('请输入要测试的功能（INIT,BASE,FILE,TCPIP,FTP,HTTP,MQTT,SMS,PB,AUDIO,TMP），输入END结束，全选请输入ALL：')
            if fileName == 'END':
                break
            if fileName == 'ALL':
                ATListFileNames.append('INIT.txt')
                # ATListFileNames.append('BASE.txt')
                # ATListFileNames.append('FILE.txt')
                ATListFileNames.append('TCPIP.txt')
                ATListFileNames.append('FTP.txt')
                ATListFileNames.append('HTTP.txt')
                ATListFileNames.append('MQTT.txt')
                # ATListFileNames.append('SMS.txt')
                # ATListFileNames.append('PB.txt')
                # ATListFileNames.append('AUDIO.txt')
                # ATListFileNames.append('TMP.txt')
                break
            if fileName not in (
                    'INIT', 'BASE', 'FILE', 'TCPIP', 'FTP', 'HTTP', 'MQTT', 'SMS', 'PB', 'AUDIO', 'TMP', 'ALL'):
                print('输入的功能名称有误,请重新输入')
                continue
            ATListFileNames.append(fileName + '.txt')

    # 如果控制台传入的参数数量为3，格式应为python Application.py /dev/ttyUSB0 1 将相应的参数传给相应变量,并填充ATListFileNames列表
    elif len(sys.argv) == 3:
        port = sys.argv[1]
        loopTimes = int(sys.argv[2])
        ATListFileNames.append('INIT.txt')
        ATListFileNames.append('BASE.txt')
        ATListFileNames.append('FILE.txt')
        ATListFileNames.append('TCPIP.txt')
        ATListFileNames.append('FTP.txt')
        ATListFileNames.append('HTTP.txt')
        ATListFileNames.append('MQTT.txt')
        # ATListFileNames.append('SMS.txt')
        ATListFileNames.append('PB.txt')
        ATListFileNames.append('AUDIO.txt')
        # ATListFileNames.append('TMP.txt')
    else:
        print('-------------------------------------')
        print('参数有误,使用方法请添加帮助参数:-h')
        print('-------------------------------------')
        sys.exit(0)

    # 当前如果是Linux的话，询问用户是否开启trace抓取功能
    if system_cate == 'Linux':
        enable_trace = input('当前操作系统为Linux，是否抓取trace？（y/n）')
        if enable_trace == 'y':
            diag_port = input('请输入diag诊断口端口：')


    # 开启trace方法
    def start_trace():
        global diag_pid
        diag_pid = os.getpid()
        print('Run diag process' + str(diag_pid))
        os.popen("./bin/diag trace/log - - " + diag_port)


    # 如果用户是Linux系统且选择了开启trace，则新建一个进程开启trace
    print('Application process' + str(os.getpid()))
    if system_cate == 'Linux' and enable_trace == 'y':
        multiprocessing.Process(target=start_trace).start()

    # 初始化Application并执行run方法
    Application(port, baud_rate, ATListFileNames, loopTimes).run()
    # 执行完成打印
    print(str(loopTimes) + '次测试已完成')

# 用户键盘退出事件处理
except KeyboardInterrupt as ke:
    print()
    print("Exit...")
    # 同时杀死trace进程
    if system_cate == 'Linux' and enable_trace == 'y' and diag_pid != 0:
        os.kill(diag_pid, signal.SIGKILL)
    sys.exit()
# 串口异常处理
except serial.serialutil.SerialException as se:
    print(se)
    print("------------------------------")
    print(traceback.format_exc())
    if system_cate == 'Linux' and enable_trace == 'y' and diag_pid != 0:
        os.kill(diag_pid, signal.SIGKILL)
    if 'No such file or directory' in traceback.format_exc():
        print('输入的端口不存在')
    if 'PermissionError' in traceback.format_exc():
        print('端口被占用,请检查是否有其他程序正在占用设备端口')
    if 'read failed: device reports readiness' in traceback.format_exc():
        print('读取异常，建议重新连接模块测试')
# 异常处理
except Exception as e:
    if system_cate == 'Linux' and enable_trace == 'y' and diag_pid != 0:
        os.kill(diag_pid, signal.SIGKILL)
    print(e)
    print("---------------")
    print(traceback.format_exc())
