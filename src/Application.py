import ATestUtils
import ATListFileName

port = "COM4"
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


Application(port, baud_rate, ATListFileNames).run()
