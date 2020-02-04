import os


class Cmux_test:
    def __init__(self, port):
        self.port = port
        res = os.popen('./bin/cmux /dev/ttyUSB0').read()
        print(res)
