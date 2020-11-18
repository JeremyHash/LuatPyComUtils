# LuatPyComUtils

#### 介绍
使用Python构建的自动AT测试工具

#### 项目依赖
1. Python 3.6+
2. pyserial 3.4

#### 项目组成
1. 主程序：Application.py主要进行命令验证以及压力测试
2. Cmux_start.py用来开启模块的Cmux功能
3. eth_upordown_loop.py用来循环进行网卡的up or down
4. Https_download_test.py用来进行http下载压力测试
5. aliyun_test.py用来进行阿里云一机一密、一型一密测试
6. tcp_ssl_test用来进行TCP_SSL测试

#### Tips
+ ATestUtils中的res = self.ser.read(320000)里面设置的读取大小320000，一定要比你真正会返回的数据量大，不然就出现~~奇怪~~的错误

#### 感谢
<a href="https://www.jetbrains.com/?from=GoFrame"><img src="https://goframe.org/images/jetbrains.png" width="100" alt="JetBrains"/></a>