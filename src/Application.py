from utils import ATestUtils
from domain import ATListFileName
import sys

port = None
if len(sys.argv) == 1:
    print('请指定设备端口号')
    sys.exit()
if len(sys.argv) == 2:
    port = sys.argv[1]
    print("正在使用的端口号为：", port)
baud_rate = 115200
ATListFileNames = [ATListFileName.INIT, ATListFileName.TMP]


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
    print("exit...")
    sys.exit()
except Exception as e:
    print(e.__cause__)
