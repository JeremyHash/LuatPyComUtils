import os

# 读取/dev/ttyUSB* 都有哪些端口，一般只接串口的话只有一个端口，但是这个序号不确定，所以这里还是动态读一下比较合适
res1 = os.popen('ls /dev/ttyUSB*').read()
# 用bin中的cmux程序 再指定要打开的UART端口在对应的UART端口上打开CMUX功能
res2 = os.popen('./bin/cmux ' + res1).read()
print(res2)
