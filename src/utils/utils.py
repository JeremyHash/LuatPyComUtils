import binascii


# 字符串转十六进制字符串方法
def str_to_hexStr(string):
    str_bin = string.encode('GB2312')
    return binascii.hexlify(str_bin)


# 字节数据转十六进制方法
def get_hex(bytes_data):
    l = [hex(i) for i in bytes_data]
    return " ".join(l)


# 十六进制字符串转字符串方法
def hexStr_to_str(hex_str):
    hex = hex_str.encode('GB2312')
    str_bin = binascii.unhexlify(hex)
    return str_bin.decode('GB2312')


if __name__ == '__main__':
    print(hexStr_to_str('41542b43474154543f'))
    print(get_hex(b'AT'))
    print(str_to_hexStr('AT+CGATT?'))

    for i in b'AT':
        print(hex(i))
