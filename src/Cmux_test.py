import os


class Cmux_test:
    def __init__(self, port):
        self.port = port
        res = os.popen('./bin/cmux %s' % port).read()
        print(res)


Cmux_test('/dev/ttyUSB0')
