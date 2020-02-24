import os


class Auto:

    def get_com(self, com_name):
        port = os.popen(f".././bin/dev_name {com_name}").read()
        return port
