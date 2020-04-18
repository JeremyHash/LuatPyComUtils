# JeremyPyComUtils

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
