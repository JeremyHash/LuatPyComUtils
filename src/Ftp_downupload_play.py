import traceback
from utils import Logger
import sys


# FTP测试
class Ftp_play_upload:
    log = Logger.Logger('./log/FTP.txt', level='debug')
    uploadfile = ''
    downloadfile = ''

    # 构造方法
    def __init__(self, ser, num):
        self.ser = ser
        self.num = num

    # 播放
    def setbreak(self):
        file = open("static/call.mp3", "rb")
        row = file.read(10240)
        self.ser.timeout = 0.5
        cmd = b'AT+FSCREATE="call.mp3"\r\n'
        self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
        cmd = b'AT+FSWRITE="call.mp3",0,10240,20\r\n'
        self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
        cmd = b'%s' % row
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")
        cmd = b'AT+CAUDPLAY=1,"call.mp3"\r\n'
        self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")

        if self.num >= 1:
            #获取upload文件大小
            cmd = b'AT+FTPSIZE\r\n'
            self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
            self.ser.write(cmd)
            self.ser.timeout = 5
            self.uploadfile = self.ser.read(200).decode(encoding='GB2312')
            self.uploadfile = self.uploadfile.split('\r\n')[4].split(',')[2]
            self.ser.timeout = 0.5
            cmd = b'AT\r\n'
            self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
            self.ser.write(cmd)
            self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")

            # 获取download文件大小
            cmd = b'AT+FTPGETTOFS=0,"call.mp3"\r\n'
            self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
            self.ser.write(cmd)
            self.ser.timeout = 25
            self.downloadfile = self.ser.read(200).decode(encoding='GB2312')
            self.downloadfile = self.downloadfile.split('\r\n')[4].split(',')[1]

            if int(len(row)) == int(self.uploadfile) == int(self.downloadfile):
                self.log.logger.debug(u'FTP上传下载第%d次' % self.num)
                self.log.logger.debug(u'本次FTP上传下载成功')
            else:
                self.log.logger.debug(u'FTP上传下载第%d次' % self.num)
                self.log.logger.debug(u'本次FTP上传下载失败')

        self.ser.timeout = 0.5
        cmd = b'AT+SAPBR=0,1\r\n'
        self.log.logger.debug(f"发→◇  {cmd.decode(encoding='GB2312')}")
        self.ser.write(cmd)
        self.log.logger.debug(f"收←◆  {self.ser.read(200).decode(encoding='GB2312')}")


def Ftp_play(ser, num):
    try:
        test = Ftp_play_upload(ser, num)
        test.setbreak()
    except KeyboardInterrupt as ke:
        print("exit...")
        sys.exit()
    except Exception as e:
        print(e)
        print("---------------")
        print(traceback.format_exc())
