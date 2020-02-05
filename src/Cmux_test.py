import os


class Cmux_test:
    def __init__(self):
        res1 = os.popen('ls /dev/ttyUSB*').read()
        res2 = os.popen('./bin/cmux %s' % res1).read()
        print(res2)


Cmux_test()
