# import binascii
#
# def hexStr_to_str(hex_str):
#     hex = hex_str.encode('utf-8')
#     str_bin = binascii.unhexlify(hex)
#     return str_bin.decode('utf-8')
#
# print(hexStr_to_str('4154').encode('gb2312'))

import hmac
message = b'clientId862991419835241deviceName862991419835241productKeyb0FMK1Ga5cp'
key = b'y7MTCG6Gk33Ux26bbWSpANl4OaI0bg5Q'
h = hmac.new(key,message,digestmod='MD5')
print(h.hexdigest())