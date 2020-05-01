import binascii


def str_to_hexStr(string):
    str_bin = string.encode('utf-8')
    return binascii.hexlify(str_bin)


def get_hex(bytes_data):
    l = [hex(i) for i in bytes_data]
    return " ".join(l)


def hexStr_to_str(hex_str):
    hex = hex_str.encode('utf-8')
    str_bin = binascii.unhexlify(hex)
    return str_bin.decode('utf-8')

print(hexStr_to_str('41542b43474154543f'))
print(get_hex(b'AT'))
print(str_to_hexStr('AT+CGATT?'))
#
# for i in b'AT':
#     print(hex(i))