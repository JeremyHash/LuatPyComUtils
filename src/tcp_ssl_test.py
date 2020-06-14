import serial
import binascii
from utils import Logger


log = Logger.Logger('./log/tcp_ssl_test.txt', level='debug').logger


def tcp_ssl_test(port):
    s = serial.Serial(port, baudrate=115200)

    s.timeout = 2
    cmd_tmp = b'1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890'
    s.write(cmd_tmp)
    log.debug(s.read(10000).decode())
    cmd_tmp = b'AT^TRACECTRL=0,1,3\r\n'
    s.write(cmd_tmp)
    log.debug(s.read(10000).decode())
    cmd_tmp = b'AT+CIPSHUT\r\n'
    s.write(cmd_tmp)
    log.debug(s.read(10000).decode())

    cmd1 = b"AT+FSCREATE=server.crt\r\n"
    s.write(cmd1)
    log.debug(s.read(10000).decode())

    cmd2 = b"AT+FSWRITE=server.crt,0,1285,20\r\n"
    s.write(cmd2)
    log.debug(s.read(10000).decode())

    cmd3 = b"-----BEGIN CERTIFICATE-----\nMIIDhzCCAvCgAwIBAgIJAJVqp5Z9Aim1MA0GCSqGSIb3DQEBBQUAMIGKMQswCQYD\nVQQGEwJDTjERMA8GA1UECBMIU2hhbmdIYWkxETAPBgNVBAcTCFNoYW5nSGFpMQ8w\nDQYDVQQKEwZhaXJtMm0xDTALBgNVBAsTBHNvZnQxDzANBgNVBAMTBnNlbGZDQTEk\nMCIGCSqGSIb3DQEJARYVemh1dGlhbmh1YUBhaXJtMm0uY29tMB4XDTE4MDExMjA2\nMzM1N1oXDTI4MDExMDA2MzM1N1owgYoxCzAJBgNVBAYTAkNOMREwDwYDVQQIEwhT\naGFuZ0hhaTERMA8GA1UEBxMIU2hhbmdIYWkxDzANBgNVBAoTBmFpcm0ybTENMAsG\nA1UECxMEc29mdDEPMA0GA1UEAxMGc2VsZkNBMSQwIgYJKoZIhvcNAQkBFhV6aHV0\naWFuaHVhQGFpcm0ybS5jb20wgZ8wDQYJKoZIhvcNAQEBBQADgY0AMIGJAoGBALqX\n/4SCaPX1K9/0r3BiK3kfgW48OntIo4qbpiIlvozwhCv+qCKcvntJ9jn6PznDEzHi\nuIBJh3adt7D32l2ncKwO85krmhFAeYqUzWRFujPuMAAEwK010IMdVcREfaAiudzI\nfPh/jpPel3Eu2bunDGYDRWiFNMainfxhOyoy3I27AgMBAAGjgfIwge8wHQYDVR0O\nBBYEFMf8PqOq5B/Y1Sqz0ksgJuFKI0HTMIG/BgNVHSMEgbcwgbSAFMf8PqOq5B/Y\n1Sqz0ksgJuFKI0HToYGQpIGNMIGKMQswCQYDVQQGEwJDTjERMA8GA1UECBMIU2hh\nbmdIYWkxETAPBgNVBAcTCFNoYW5nSGFpMQ8wDQYDVQQKEwZhaXJtMm0xDTALBgNV\nBAsTBHNvZnQxDzANBgNVBAMTBnNlbGZDQTEkMCIGCSqGSIb3DQEJARYVemh1dGlh\nbmh1YUBhaXJtMm0uY29tggkAlWqnln0CKbUwDAYDVR0TBAUwAwEB/zANBgkqhkiG\n9w0BAQUFAAOBgQCur2oMUFvtWrrE5ncwasuTpGA32zMojvh8aTE6MnBQYiafm4zc\n85sAUyd0Gdf7yh+pNgv7PuXNy7MDcr4vr01SEJhIqlDJK0Pe42CxzvEJ2hbwLFLp\nu/Sy5rdmX/Bpj6luHqkCsngEeS0PPsvlKFJUZBSRVI/DgPpyiTuaOEIrQA==\n-----END CERTIFICATE-----\n"
    s.write(cmd3)
    log.debug(s.read(10000).decode())

    cmd4 = b"AT+FSREAD=server.crt,0,10240,0\r\n"
    s.write(cmd4)
    log.debug(s.read(10000).decode())

    cmd5 = b"AT+FSCREATE=client.crt\r\n"
    s.write(cmd5)
    log.debug(s.read(10000).decode())

    cmd6 = b"AT+FSWRITE=client.crt,0,1118,20\r\n"
    s.write(cmd6)
    log.debug(s.read(10000).decode())

    cmd7 = b"-----BEGIN CERTIFICATE-----\r\nMIIC/zCCAmigAwIBAgIBAjANBgkqhkiG9w0BAQUFADCBijELMAkGA1UEBhMCQ04x\r\nETAPBgNVBAgTCFNoYW5nSGFpMREwDwYDVQQHEwhTaGFuZ0hhaTEPMA0GA1UEChMG\r\nYWlybTJtMQ0wCwYDVQQLEwRzb2Z0MQ8wDQYDVQQDEwZzZWxmQ0ExJDAiBgkqhkiG\r\n9w0BCQEWFXpodXRpYW5odWFAYWlybTJtLmNvbTAeFw0xODAxMTIwNjUwNDBaFw0y\r\nODAxMTAwNjUwNDBaMIGCMQswCQYDVQQGEwJDTjERMA8GA1UECBMIU2hhbmdIYWkx\r\nDzANBgNVBAoTBmFpcm0ybTENMAsGA1UECxMEc29mdDEaMBgGA1UEAxQRemh1dGlh\r\nbmh1YV9jbGllbnQxJDAiBgkqhkiG9w0BCQEWFXpodXRpYW5odWFAYWlybTJtLmNv\r\nbTCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEA3Tum2kgr02gHzQlwrMYxAA2e\r\nqZsTE6oaWIwKrrpeHPTPGvGe15bVLRjVJFi7mYXWIpqhznBK6kIgLSdUGJYpDzdg\r\ns8PU4/c8usk3Rmv11kwRps31brcaqQ/eMTE9P8pZizwY02vkSWDgk9A62yS2Pav8\r\n1E/DWS/dsJvE79n6+t8CAwEAAaN7MHkwCQYDVR0TBAIwADAsBglghkgBhvhCAQ0E\r\nHxYdT3BlblNTTCBHZW5lcmF0ZWQgQ2VydGlmaWNhdGUwHQYDVR0OBBYEFA0nZpzk\r\nxApUtQfPyIa7bD6bsky7MB8GA1UdIwQYMBaAFMf8PqOq5B/Y1Sqz0ksgJuFKI0HT\r\nMA0GCSqGSIb3DQEBBQUAA4GBAENH2PvCcZzljSqZHAW91+WCmwHOlS2PQp86Ak5B\r\n9CoH6N6jdIsaXVPQwPELzmWhFf2XvRV1Fiq5BGjoPLW8OlMsrIFciETqUvbqvN+w\r\n1GHi73zyCaCV+M8dMcdR+3Odue5S0hrtHdhliodSqYCT1mA8go8cEAM8uc9h6jpA\r\ni1Ka\r\n-----END CERTIFICATE-----\r\n"
    s.write(cmd7)
    log.debug(s.read(10000).decode())

    cmd8 = b"AT+FSREAD=client.crt,0,1118,2\r\n"
    s.write(cmd8)
    log.debug(s.read(10000).decode())

    cmd9 = b"AT+FSCREATE=client.key\r\n"
    s.write(cmd9)
    log.debug(s.read(10000).decode())

    cmd10 = b"AT+FSWRITE=client.key,0,887,20\r\n"
    s.write(cmd10)
    log.debug(s.read(10000).decode())

    cmd11 = b"-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQDdO6baSCvTaAfNCXCsxjEADZ6pmxMTqhpYjAquul4c9M8a8Z7X\nltUtGNUkWLuZhdYimqHOcErqQiAtJ1QYlikPN2Czw9Tj9zy6yTdGa/XWTBGmzfVu\ntxqpD94xMT0/ylmLPBjTa+RJYOCT0DrbJLY9q/zUT8NZL92wm8Tv2fr63wIDAQAB\nAoGAHoh+FcBCNDI2aWj1IRNVbfFzRWs+rccbTb8+NjFIjeyHrOtOBekuUMQNnq+U\nbLLZA/ude1VqMXyg3jqAU8hdsBcyGaTLXgX5XoEvFwisR4tivW5p8tG8q/ZqOCs1\nWoXG2yyPBt+mLa4mujNmWGnS+sNgi51n+L8rWOkxW2we4gECQQD3YO+fjkqPDkKP\nB6tZTNYD3JrR35/6Yw1LaIjYO+EYvbQPEy+ZQRanZU/w/rEHDgqLobs+qDoa8cvq\nXavGNf3fAkEA5PFzDonv5BvjrYgo0hehj8b7XdUvdQpRcQR1KfN7E/NiBK9GhGge\n3/ZCe0grlTKOXWzCWReNCNybg75AcOCjAQJAJ8EoQRf422yLPbkZzEwQyKYXK0so\nxnBMnqW5+CYHUpaJ7TJEH/jZzyT05+HGST/0aeQf1z3puJLLFmrfRAdBOQJAQX5A\n59vV4G+KBk55PwC7myHVLtaZqOW2vpoD2mhowSBS3fw2NBKFIpSUGChhL2EzEM7Y\nGhx+oBZb9qgqTyA0AQJBAIwdm6xlaD4gjA/BciK3knIRUaGkINrNDnhAh4ObUnuf\nOHriSGx89nYxZYwWuvO1Ed4oSMkRaARdS8Vw2/XUS90=\n-----END RSA PRIVATE KEY-----\n"
    s.write(cmd11)
    log.debug(s.read(10000).decode())

    cmd12 = b"AT+FSREAD=client.key,0,887,0\r\n"
    s.write(cmd12)
    log.debug(s.read(10000).decode())

    s.timeout = 1
    cmd_tmp = b'AT+SSLCFG="seclevel",1,1\r\n'
    s.write(cmd_tmp)
    log.debug(s.read(10000).decode())
    cmd_tmp = b'AT+SSLCFG="cacert",1,"server.crt"\r\n'
    s.write(cmd_tmp)
    log.debug(s.read(10000).decode())
    cmd_tmp = b'AT+SSLCFG="seclevel",2,2\r\n'
    s.write(cmd_tmp)
    log.debug(s.read(10000).decode())
    cmd_tmp = b'AT+SSLCFG="cacert",2,"server.crt"\r\n'
    s.write(cmd_tmp)
    log.debug(s.read(10000).decode())
    cmd_tmp = b'AT+SSLCFG="clientcert",2,"client.crt"\r\n'
    s.write(cmd_tmp)
    log.debug(s.read(10000).decode())
    cmd_tmp = b'AT+SSLCFG="clientkey",2,"client.key"\r\n'
    s.write(cmd_tmp)
    log.debug(s.read(10000).decode())
    # cmd_tmp = b'AT+CIPMODE=0\r\n'
    # s.write(cmd_tmp)
    # print(s.read(10000))
    cmd_tmp = b'AT+CIPMUX=1\r\n'
    s.write(cmd_tmp)
    log.debug(s.read(10000).decode())
    cmd_tmp = b'AT+CIPSSL=1\r\n'
    s.write(cmd_tmp)
    log.debug(s.read(10000).decode())
    cmd_tmp = b'AT+CSTT\r\n'
    s.write(cmd_tmp)
    log.debug(s.read(10000).decode())
    cmd_tmp = b'AT+CIICR\r\n'
    s.write(cmd_tmp)
    log.debug(s.read(10000).decode())
    cmd_tmp = b'AT+CIFSR\r\n'
    s.write(cmd_tmp)
    log.debug(s.read(10000).decode())

    while True:
        cmd_tmp = b'AT+CIPSTART=1,"TCP","36.7.87.100",4433\r\n'
        s.write(cmd_tmp)
        log.debug("发→◇" + cmd_tmp.decode())
        log.debug("收←◆" + s.read(10000).decode())
        cmd_tmp = b'AT+CIPSTART=2,"TCP","36.7.87.100",4434\r\n'
        s.write(cmd_tmp)
        log.debug("发→◇" + cmd_tmp.decode())
        log.debug("收←◆" + s.read(10000).decode())
        s.timeout = 1
        cmd_tmp = b'AT+CIPSEND=1,61\r\n'
        s.write(cmd_tmp)
        log.debug("发→◇" + cmd_tmp.decode())
        log.debug("收←◆" + s.read(10000).decode())
        s.timeout = 8
        cmd_tmp = b'GET / HTTP/1.1\r\nHost: 36.7.87.100\r\nConnection: keep-alive\r\n\r\n'
        s.write(cmd_tmp)
        log.debug("发→◇" + cmd_tmp.decode())
        log.debug("收←◆" + s.read(10000).decode())
        s.timeout = 1
        cmd_tmp = b'AT+CIPSEND=2,61\r\n'
        s.write(cmd_tmp)
        log.debug("发→◇" + cmd_tmp.decode())
        log.debug("收←◆" + s.read(10000).decode())
        s.timeout = 8
        cmd_tmp = b'GET / HTTP/1.1\r\nHost: 36.7.87.100\r\nConnection: keep-alive\r\n\r\n'
        s.write(cmd_tmp)
        log.debug("发→◇" + cmd_tmp.decode())
        log.debug("收←◆" + s.read(10000).decode())
        s.timeout = 3
        cmd_tmp = b'AT+CIPCLOSE=1\r\n'
        s.write(cmd_tmp)
        log.debug("发→◇" + cmd_tmp.decode())
        log.debug("收←◆" + s.read(10000).decode())
        cmd_tmp = b'AT+CIPCLOSE=2\r\n'
        s.write(cmd_tmp)
        log.debug("发→◇" + cmd_tmp.decode())
        log.debug("收←◆" + s.read(10000).decode())


if __name__ == '__main__':
    port = input("请输入测试端口：")
    tcp_ssl_test(port)
