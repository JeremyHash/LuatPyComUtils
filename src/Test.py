import re
import sys

# m = re.match(r'.*\s{4}OK\s{2}', 'ATE1\r\n\r\nOK\r\n')
# print(m)
# print('AT+CREG?;+CEREG?;+CGREG?====AT\+CREG\?;\+CEREG\?;\+CGREG\?\s{4}\+CREG: (?:.|\n)*\s{4}OK\s{2}====1'.split('====')[2])
# tmp1 = 'productKey=a17d2LpfCVD&sign=a69dcca8f05e1df41f06bc9ea199ab14&clientId=CcepH48uP4BCUXWpkD92&deviceName=CcepH48uP4BCUXWpkD92'
# tmp2 = 'productKey=a17d2LpfCVD&deviceName=CcepH48uP4BCUXWpkD92&random=123456&sign=d98e1fc1cc380f9c8fa5e3c051fcb75b&signMethod=HmacMD5'
# tmp3 = 'productKey=a17d2LpfCVD&sign=33f77aab2d54ac05da0a5bc95bf9f2d6&clientId=CcepH48uP4BCUXWpkD92&deviceName=CcepH48uP4BCUXWpkD92'
# print(len(tmp3))
print(sys.argv[0])
print(len(sys.argv))
