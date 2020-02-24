import os


class Auto:

    def get_com(self, com_name):
        port = os.popen(f".././bin/dev_name {com_name}").read()
        return port


if __name__ == '__main__':
    com_name = input('请输入要识别的端口：')
    port = Auto().get_com(com_name)
    print(f'端口号为：{port}')
