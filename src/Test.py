import re

# m = re.match('OK', '\r\nOK\r\n'.strip())
# print(m)
print('AT+CREG?;+CEREG?;+CGREG?====AT\+CREG\?;\+CEREG\?;\+CGREG\?\s{4}\+CREG: (?:.|\n)*\s{4}OK\s{2}====1'.split('====')[2])
