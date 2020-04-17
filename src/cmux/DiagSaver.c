/*
 * DiagSaver application
 *
 * Marvell Diag log saver on Linux - 1.0.0.0
 *
 * Copyright (C) 1995-2014 Marvell.Co.,LTD
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <termios.h>
#include <time.h>
#include <signal.h>
#include <sys/time.h>
#include <sys/stat.h>

#include <sys/socket.h>
#include <sys/types.h>
#include <arpa/inet.h>

#include <netinet/in.h>
#include <netdb.h>

#include <libgen.h>
#include <sys/inotify.h>

#include <poll.h>
/* #include <libudev.h> */

#include "tool.h"

#define _FILE_SIZE 200 //2MB

#define EXIT(name)          \
    do                      \
    {                       \
        perror(name);       \
        exit(EXIT_FAILURE); \
    } while (0)

char filename[256] = {0};
char path[256] = "/dev/";
FILE *fp = NULL;
int sockfd;
int useSocket;
int fd;
unsigned int g_uiFileIndex = 0x0;

/* struct udev *udevp;
struct udev_monitor *monp;
int monitorfd;
char udevpath[256] = {0}; */

struct CSDLFileHeader
{
    unsigned int dwHeaderVersion; //0x0
    unsigned int dwDataFormat;    //0x1
    unsigned int dwAPVersion;
    unsigned int dwCPVersion;
    unsigned int dwSequenceNum;
    unsigned int dwTime;     //Total seconds from 1970.1.1 0:0:0
    unsigned int dwCheckSum; //0x0
};

int openport(char *pszDeviceName)
{
    int fd = open(pszDeviceName, O_RDWR | O_SYNC | O_NOCTTY | O_NDELAY);
    if (-1 == fd)
    {
        perror("Can't Open Diag device!");
        return -1;
    }
    else
    {
        ////tprintf (_T("\nOpened Diag DeviceName : %s\n"),pszDeviceName);
        return fd;
    }
}

int setport(int fd, int baud, int databits, int stopbits, int parity)
{
    int baudrate;
    struct termios newtio;
    switch (baud)
    {
    case 300:
        baudrate = B300;
        break;
    case 600:
        baudrate = B600;
        break;
    case 1200:
        baudrate = B1200;
        break;
    case 2400:
        baudrate = B2400;
        break;
    case 4800:
        baudrate = B4800;
        break;
    case 9600:
        baudrate = B9600;
        break;
    case 19200:
        baudrate = B19200;
        break;
    case 38400:
        baudrate = B38400;
        break;
    default:
        baudrate = B9600;
        break;
    }
    tcgetattr(fd, &newtio);
    bzero(&newtio, sizeof(newtio));
    //setting   c_cflag
    newtio.c_cflag &= ~CSIZE;
    switch (databits)
    {
    case 7:
        newtio.c_cflag |= CS7;
        break;
    case 8:
        newtio.c_cflag |= CS8;
        break;
    default:
        newtio.c_cflag |= CS8;
        break;
    }
    switch (parity) //????У??
    {
    case 'n':
    case 'N':
        newtio.c_cflag &= ~PARENB; /* Clear parity enable */
        newtio.c_iflag &= ~INPCK;  /* Enable parity checking */
        break;
    case 'o':
    case 'O':
        newtio.c_cflag |= (PARODD | PARENB);
        newtio.c_iflag |= INPCK; /* Disnable parity checking */
        break;
    case 'e':
    case 'E':
        newtio.c_cflag |= PARENB; /* Enable parity */
        newtio.c_cflag &= ~PARODD;
        newtio.c_iflag |= INPCK; /* Disnable parity checking */
        break;
    case 'S':
    case 's': /*as no parity*/
        newtio.c_cflag &= ~PARENB;
        newtio.c_cflag &= ~CSTOPB;
        break;
    default:
        newtio.c_cflag &= ~PARENB; /* Clear parity enable */
        newtio.c_iflag &= ~INPCK;  /* Enable parity checking */
        break;
    }
    switch (stopbits)
    {
    case 1:
        newtio.c_cflag &= ~CSTOPB; //1
        break;
    case 2:
        newtio.c_cflag |= CSTOPB; //2
        break;
    default:
        newtio.c_cflag &= ~CSTOPB;
        break;
    }
    newtio.c_cc[VTIME] = 0;
    newtio.c_cc[VMIN] = 0;
    newtio.c_cflag |= (CLOCAL | CREAD);
    //newtio.c_oflag|=OPOST;
    newtio.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG); //Input, RawData mode
    newtio.c_oflag &= ~OPOST;                          //Output
    newtio.c_iflag &= ~(IXON | IXOFF | IXANY);
    cfsetispeed(&newtio, baudrate);
    cfsetospeed(&newtio, baudrate);
    tcflush(fd, TCIFLUSH);
    if (tcsetattr(fd, TCSANOW, &newtio) != 0)
    {
        perror("SetupSerial 3");
        return -1;
    }
    return 0;
}

int writeport(int fd, char *buf, int len)
{
    int i;
    write(fd, buf, len);
    printf("Send CMD to UE: ");
    for (i = 0; i < 16; i++)
        printf("0x%2X ", buf[i]);
    printf("\n");
    return 0;
}

void clearport(int fd)
{
    tcflush(fd, TCIOFLUSH);
}

int readport(int fd, char *buf, int maxwaittime)
{
    static struct stat statbuff;
    int rc;
    int i;
    struct timeval tv;
    fd_set readfd;
    tv.tv_sec = maxwaittime / 1000;         //SECOND
    tv.tv_usec = maxwaittime % 1000 * 1000; //USECOND
    FD_ZERO(&readfd);
    FD_SET(fd, &readfd);
    /* FD_SET(monitorfd, &readfd);
    int nfds = monitorfd > fd ? monitorfd + 1 : fd + 1; */
    rc = select(fd + 1, &readfd, NULL, NULL, &tv);
    printf("select: %d\n", rc);

    /*     if (FD_ISSET(monitorfd, &readfd))
    {
        struct udev_device *devp;
        while ((devp = udev_monitor_receive_device(monp)) != NULL)
        {
            if (strcmp(udev_device_get_action(devp), "remove") == 0)
            {
                if (strcmp(udev_device_get_sysname(devp), udevpath) == 0)
                {
                    printf("................................\n");
                    return -2;
                }
            }
        }
        rc--;
    } */

    if (rc > 0)
    {
        rc = read(fd, buf, 4096);
        printf("read: %d\n", rc);
        if (rc == -1)
        {
            perror("read");
            return -2;
        }
        //printf("recv:%d\n",rc);p
        return rc;
    }
    else
    {
        if (stat(path, &statbuff) == -1)
        {
            perror("stat");
            return -2;
        }
        return -1;
    }
}

int readport0(int fd, char *buf, int maxwaittime)
{
    struct pollfd _fd;
    static int count = 0;
    int timeout = maxwaittime;
    memset(&_fd, 0, sizeof(_fd));
    _fd.fd = fd;
    _fd.events = POLLIN;

    int ret = poll(&_fd, 1, timeout);
    if (ret < 0)
    {
        perror("poll");
        return -2;
    }
    if (ret == 0)
    {
        if (++count == 4)
            raise(SIGINT);
        return -1;
    }

    if (_fd.revents == POLLIN)
    {
        int rc = read(fd, buf, 10240);
        // printf("read: %d\n", rc);
        count = 0;
        if (rc == -1)
        {
            perror("read");
            return -2;
        }
        //printf("recv:%d\n",rc);p
        return rc;
    }
    else
    {
        printf("%d\n", _fd.revents);
        return -2;
    }
}

int savelog(char *prex, char *buf, int len)
{
    int i;
    time_t ltime;
    struct tm *currtime;
    char openmode[4] = {0};
    struct stat fileinfo;

    struct CSDLFileHeader SDLHeader;
    char *pHeader = (char *)&SDLHeader;

    // init the SDL file header
    SDLHeader.dwHeaderVersion = 0x0;
    SDLHeader.dwDataFormat = 0x1; //0x1
    SDLHeader.dwAPVersion = 0x0;
    SDLHeader.dwCPVersion = 0x0;
    SDLHeader.dwTime = 0x0;     //Total seconds from 1970.1.1 0:0:0
    SDLHeader.dwCheckSum = 0x0; //0x0

    if (0 == strlen(filename))
    {
        time(&ltime);

        SDLHeader.dwTime = (unsigned int)ltime;
        SDLHeader.dwSequenceNum = g_uiFileIndex; //?????????0???????

        currtime = localtime(&ltime);
        sprintf(filename, "%s_%d.sdl", prex, g_uiFileIndex);
        sprintf(openmode, "wb");

        printf("save log to %s %u\n", filename, SDLHeader.dwTime);
        fp = fopen(filename, openmode);
        // Write the file header.
        for (i = 0; i < 28; i++)
            fputc(pHeader[i], fp);
    }
    else
    {
        stat(filename, &fileinfo);
        if (fileinfo.st_size > _FILE_SIZE * 1024 * 1024 - len)
        {
            fclose(fp);
            g_uiFileIndex++; // Increse the file index
            time(&ltime);

            SDLHeader.dwTime = (unsigned int)ltime;
            SDLHeader.dwSequenceNum = g_uiFileIndex; //?????????0???????

            currtime = localtime(&ltime);
            sprintf(filename, "%s_%d.sdl", prex, g_uiFileIndex);
            sprintf(openmode, "wb");
            printf("save log to %s\n", filename);
            fp = fopen(filename, openmode);
            for (i = 0; i < 28; i++)
                fputc(pHeader[i], fp);
        }
        else
        {
            sprintf(openmode, "ab");
        }
    }

    // Write the data to current file.
    for (i = 0; i < len; i++)
        fputc(buf[i], fp);

    return 0;
}

void ctrl_c_process(int signo)
{
    printf("%s %s Got SIGINT\n", __FILE__, __FUNCTION__);
    // raise(SIGTERM);
    if (useSocket)
    {
        close(sockfd);
    }
    else
    {
        printf("close FP\n");
        fclose(fp);
    }
    printf("Exiting DiagSaver...\n");
    exit(1);
}

void savelog_socket(int sockfd, char *buff, ssize_t len)
{
    static int isFirst = 1;
    if (isFirst)
    {
        time_t ltime;
        struct CSDLFileHeader SDLHeader;
        char *pHeader = (char *)&SDLHeader;

        // init the SDL file header
        SDLHeader.dwHeaderVersion = 0x0;
        SDLHeader.dwDataFormat = 0x1; //0x1
        SDLHeader.dwAPVersion = 0x0;
        SDLHeader.dwCPVersion = 0x0;
        SDLHeader.dwTime = 0x0;     //Total seconds from 1970.1.1 0:0:0
        SDLHeader.dwCheckSum = 0x0; //0x0

        time(&ltime);
        SDLHeader.dwTime = (unsigned int)ltime;

        write(sockfd, pHeader, sizeof(SDLHeader));

        isFirst = 0;
    }

    if (write(sockfd, buff, len) < 0)
        EXIT("write");
}

void init_sockaddr(struct sockaddr_in *addr, char *hostname, int port)
{
    struct hostent *hostinfo;
    addr->sin_family = AF_INET;
    addr->sin_port = htons(port);
    hostinfo = gethostbyname(hostname);
    if (hostinfo == NULL)
        EXIT("gethostbyname");
    addr->sin_addr = *(struct in_addr *)hostinfo->h_addr;
}

char *devname()
{
    const char *name = dev_name(E_DIAG);
    if (name == NULL)
    {
        printf("no interface\n");
        exit(EXIT_FAILURE);
    }
    strcat(path, name);
    /* strcat(udevpath, name); */
    return path;
}

int main(int argc, char **argv)
{
    int rc, i, ret, readlen;
    int optc;
    char *fileName;

    char *hostname;
    int servport;

    freopen("/dev/null", "w", stdout);

    readlen = 0;
    unsigned char rbuf[10240] = {0};
    unsigned char ACATReady[16] = {0x10, 0x00, 0x00, 0x00, 0x00, 0x04, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};  // ACAT Ready command
    unsigned char GetAPDBVer[16] = {0x10, 0x00, 0x00, 0x00, 0x80, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}; // Get AP DB Ver command
    unsigned char GetCPDBVer[16] = {0x10, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}; // Get CP DB Ver command
    //char dev[256];
    char *dev;

    // Capture the Ctrl+C
    struct sigaction act;
    act.sa_handler = ctrl_c_process;
    act.sa_flags = 0;

    // signal(SIGTERM, ctrl_c_process);

    if (sigaction(SIGINT, &act, NULL) < 0)
    {
        printf("Install Signal Action Error: %s \n", strerror(errno));
        return 0;
    }

    if (argc == 2 || argc == 3 || argc == 4)
    {
        dev = devname();
    }
    else if (argc == 5)
    {
        dev = argv[4];
    }
    
    printf("%s %s %s\n", __FILE__, __FUNCTION__, dev);
    // dev = argv[1];

    if (argc == 3 || argc == 4)
    {
        int type;

        useSocket = 1;
        hostname = argv[1];
        servport = atoi(argv[2]);

        if (argc == 3)
            type = SOCK_STREAM;
        else
            type = SOCK_DGRAM;

        struct sockaddr_in addr;
        memset((char *)&addr, 0, sizeof(addr));
        sockfd = socket(AF_INET, type, 0);
        if (sockfd < 0)
            EXIT("socket");
        init_sockaddr(&addr, hostname, servport);
        if (connect(sockfd, (struct sockaddr *)&addr, sizeof(addr)) == -1)
            EXIT("connect");
    }
    else if (argc == 2 || argc == 5)
    {
        fileName = argv[1];
        printf("save Air720 Log to %s_x.sdl\n", fileName);
    }
    else
    {
        printf("usage\n ./diag logname\n ./diag hostname port\n ./diag hostname port flag(ignored)\n");
        exit(-1);
    }

    //Open Diag device
    fd = openport(dev);

    if (fd > 0)
    {
        printf("Opened the device %s\n", dev);
        if (strstr(dev, "MDiagUSB") == NULL)
        {
            ret = setport(fd, 115200, 8, 1, 'n'); //Set serial port
            if (ret < 0)
            {
                printf("Can't Set Serial Port!\n");
                return 0;
            }
            else
            {
                printf("Set Serial Port Done.\n");
            }
        }
    }
    else
    {
        printf("Can't Open Serial Port!\n");
        return 0;
    }

    /* udevp = udev_new();
    if (!udevp)
    {
        printf("can't create udev");
        return 1;
    }
    monp = udev_monitor_new_from_netlink(udevp, "kernel");
    udev_monitor_filter_add_match_subsystem_devtype(monp, "tty", NULL);
    udev_monitor_enable_receiving(monp);
    monitorfd = udev_monitor_get_fd(monp); */

    //Send the ACAT Ready to UE
    writeport(fd, ACATReady, 16);
    usleep(200);
    writeport(fd, GetAPDBVer, 16);
    usleep(300);
    writeport(fd, GetCPDBVer, 16);

    printf("Sent CMD, receiving data. Press Ctrl+C to exit.\n");
    while (1)
    {
        // rc = readport0(fd, rbuf, 2000); //Read data, timeout is 500 ms
        rc = read(fd, rbuf, 10240);
        printf("read: %d\n", rc);
        if (rc > 0)
        {
            //for(i=0;i<rc;i++)
            //	printf("%02x ",rbuf[i]);
            //printf("\n");

            if (useSocket)
            {
                savelog_socket(sockfd, rbuf, rc);
            }
            else
            {
                savelog(fileName, rbuf, rc);
            }
        }
        else
        {
            if (rc == -1)
            {
                perror("read");
                break;
            }
            printf("recv none, data length: %d Bytes\n", rc);
            sleep(1);
        }
    }
    if (useSocket)
    {
        close(sockfd);
    }
    else
    {
        fclose(fp);
    }

    return 0;
}
