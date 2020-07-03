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
#include <pthread.h>

#include <netinet/in.h>
#include <netdb.h>

#include <libgen.h>
#include <sys/inotify.h>

#include <poll.h>
/* #include <libudev.h> */

#include "usb_find.h"
static pthread_t pppd_thread;
static pthread_t pppd_thread_AP;
struct CH_TIMESTAMP  timeStamp ;
struct CH_TIMESTAMP * add_time_stamp();


#define _FILE_SIZE 10 //10MB
#define _FILE_SIZE_CP 200 //10MB


#define EXIT(name)          \
    do                      \
    {                       \
        perror(name);       \
        exit(EXIT_FAILURE); \
    } while (0)

char filename[256] = {0};
	
char filename1[256] = {0};
char path0[256] = "/dev/";
char pathtest[256] = "/dev/";

char path[256] = "/dev/";
char path_CP[256] = "/dev/";

FILE *fp = NULL;
FILE *fpcp = NULL;

int sockfd;
int useSocket;
int fd;
int fdcp;
int fdat;
char *fileName;
#define CATCH_CP_LOG 1
 struct CH_TIMESTAMP {
 unsigned char sync;
 unsigned char lenM;
 unsigned char lenL;
 unsigned char flowid;
 unsigned int date;
 unsigned int ms;
};

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
        printf("Can't Open Diag device! %s",pszDeviceName);
        return -1;
    }
    else
    {
        ////tprintf (_T("\nOpened Diag DeviceName : %s\n"),pszDeviceName);
        return fd;
    }
}

static int create_thread(pthread_t * thread_id, void * thread_function, void * thread_function_arg ) {
    static pthread_attr_t thread_attr;
    pthread_attr_init(&thread_attr);
    pthread_attr_setdetachstate(&thread_attr, PTHREAD_CREATE_DETACHED);
    if (pthread_create(thread_id, &thread_attr, thread_function, thread_function_arg)!=0) {
        LOGE("%s %s errno: %d (%s)", __FILE__, __func__, errno, strerror(errno));
        return 1;
    }
    pthread_attr_destroy(&thread_attr); /* Not strictly necessary */
    return 0; //thread created successfully
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
    printf("Send CMD to UE: \n");
	for (i = 0; i < len; i++)
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

int savelog(char *prex, char *buf, int len , int type)
{
    int i;
    time_t ltime;
    struct tm *currtime;
    char openmode[4] = {0};
    struct stat fileinfo;
	void * times = NULL;

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
        sprintf(filename, "%s_%02d:%02d:%02d.bin", prex, currtime->tm_hour, currtime->tm_min, currtime->tm_sec);
        sprintf(openmode, "wb");

        printf("save log to %s %u\n", filename, SDLHeader.dwTime);
        fp = fopen(filename, openmode);
		times = (void *)add_time_stamp();
	    for (i = 0; i < sizeof(struct tm); i++)
	        fputc(*(unsigned char *)(times+i), fp);

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
            sprintf(filename, "%s_%02d:%02d:%02d.bin", prex, currtime->tm_hour, currtime->tm_min, currtime->tm_sec);
            sprintf(openmode, "wb");
            printf("save log to %s\n", filename);
            fp = fopen(filename, openmode);
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


int savecplog(char *buf, int len , int type)
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

    if (0 == strlen(filename1))
    {
        time(&ltime);

        SDLHeader.dwTime = (unsigned int)ltime;
        SDLHeader.dwSequenceNum = g_uiFileIndex; //?????????0???????

        currtime = localtime(&ltime);
        sprintf(filename1, "Arm(%02d-%02d-%02d-%02d-00).Sn(0).tra", currtime->tm_mday, currtime->tm_hour, currtime->tm_min, currtime->tm_sec);
        sprintf(openmode, "wb");

        printf("save log to %s %u\n", filename1, SDLHeader.dwTime);
        fpcp  = fopen(filename1, openmode);

    }
    else
    {
        stat(filename1, &fileinfo);
        if (fileinfo.st_size > _FILE_SIZE_CP * 1024 * 1024 - len)
        {
            fclose(fpcp );
            g_uiFileIndex++; // Increse the file index
            time(&ltime);

            SDLHeader.dwTime = (unsigned int)ltime;
            SDLHeader.dwSequenceNum = g_uiFileIndex; //?????????0???????

            currtime = localtime(&ltime);
			sprintf(filename1, "Arm(%02d-%02d-%02d-%02d-00).Sn(0).tra", currtime->tm_mday, currtime->tm_hour, currtime->tm_min, currtime->tm_sec);
            sprintf(openmode, "wb");
            printf("save log to %s\n", filename1);
            fpcp  = fopen(filename1, openmode);
        }
        else
        {
            sprintf(openmode, "ab");
        }
    }

    // Write the data to current file.
    for (i = 0; i < len; i++)
        fputc(buf[i], fpcp );

    return 0;
}



static void* cp_thread_function(void*  arg) {
    char **argvv = (char **)arg;
    char serialdevname[32];
    char cgdcont_cmd[256];
	int rc1;
	printf("pppd_thread_function\n" );
    unsigned char rcpbuf[10240] = {0};
    int count = 0;


	
    while (1) 
  	{

		rc1 = read(fdcp, rcpbuf, 10240);
		
        printf("read fdcp: %d\n", rc1);
		if (rc1 > 0 )
		{
			//for(i=0;i<rc;i++)
			//	printf("%02x ",rbuf[i]);
			//printf("\n");
		
			if (useSocket)
			{
				savelog_socket(sockfd, rcpbuf, rc1);
			}
			else
			{
				savecplog(rcpbuf, rc1, rc1);
			}
		}
		else
		{
			/*if (rc1 == -1)
			{
				perror("read");
				break;
			}*/
			printf("recv none, data length: %d Bytes\n", rc1);
			sleep(1);
		}

	}

    pppd_thread = 0;
    LOGD("%s exit", __func__);
    pthread_exit(NULL);
    return NULL;         
}

struct CH_TIMESTAMP * add_time_stamp()
{
    time_t ltime;
    struct tm *currtime;
	
	time(&ltime);
	currtime = localtime(&ltime);
	timeStamp.sync = 0xad;
	timeStamp.lenM = 0;
	timeStamp.lenL = 0X08;
	timeStamp.flowid = 0XA2;
	timeStamp.date = 0;
	timeStamp.date = ((currtime->tm_year  + 1900) << 16) +  (currtime->tm_mon << 8) +  currtime->tm_mday;
	timeStamp.ms  =  currtime->tm_hour * 60 *60*1000  + currtime->tm_min *60*1000 + currtime->tm_sec *1000;
    LOGD("tm_year %d  tm_mon %d tm_mday %d", currtime->tm_year + 1900 , currtime->tm_mon ,currtime->tm_mday);
    LOGD("tm_hour %d  tm_min %d tm_sec %d", currtime->tm_hour , currtime->tm_min ,currtime->tm_sec);

	return  &timeStamp;
}

static void* ap_thread_function(void*  arg) {
    char **argvv = (char **)arg;
    char serialdevname[32];
    char cgdcont_cmd[256];
	int rc;
	int nums = 0;
	printf("pppd_thread_function\n" );
    unsigned char apbuf[10240] = {0};
    int count = 0;
	time_t oldtime;
	time_t newtime;
	time(&oldtime);


	
    while (1) 
  	{

		rc = read(fd, apbuf, 10240);
		
        printf("read ap: %d\n", rc);
		if (rc > 0 )
		{	
			time(&oldtime);
			//for(i=0;i<rc;i++)
			//	printf("%02x ",rbuf[i]);
			//printf("\n");
		
			if (useSocket)
			{
				savelog_socket(sockfd, apbuf, rc);
			}
			else
			{
				savelog(fileName, apbuf, rc,rc);
			}
		}
		else
		{
			/*if (rc1 == -1)
			{
				perror("read");
				break;
			}*/
			time(&newtime);
			nums =  newtime - oldtime;
			
			printf("recv none, time : %d \n", nums);
			if(nums  > 1 )
				{
					time(&oldtime);
					printf("time inc is  %d\n",nums);
					savelog(fileName,(char *)add_time_stamp(),sizeof(struct CH_TIMESTAMP),sizeof(struct CH_TIMESTAMP));
				}
			sleep(1);
		}

	}

    pppd_thread = 0;
    LOGD("%s exit", __func__);
    pthread_exit(NULL);
    return NULL;         
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

char *devname(int device_interface_id,char *buf,int type)
{
    printf("%s %s\n", __FILE__, __FUNCTION__);
    const char *name = FindUsbDevice(device_interface_id);
    if (name == NULL )
    {
    	if(type != 0)
    		{
	        printf("no interface\n");
    	    exit(EXIT_FAILURE);
    		}
		else
			{
			return NULL	;
		}
    }
	strcpy(buf, "/dev/");
    strcat(buf, name);
    /* strcat(udevpath, name); */
    return buf;
}

int main(int argc, char **argv)
{
    int rc,rc1, i, ret, readlen;
    int optc;

    char *hostname;
    int servport;
    printf("%s %s  %d\n", __FILE__, __FUNCTION__,argc);

    //freopen("/dev/null", "w", stdout);

    readlen = 0;
    unsigned char rbuf[10240] = {0};
	
    unsigned char OPENCP[20] = {0x41 , 0x54, 0x2a ,0x55 , 0x53 , 0x42 , 0x3d, 0x22 , 0x43,0x50 , 0x54, 0x52, 0x41, 0x43, 0x45, 0x22, 0x2c, 0x31, 0xd, 0xa};  //AT*USB="CPTRACE",2
    
    unsigned char OPENAP[20] = {0x41,0x54,0x5e,0x54,0x52,0x41,0x43,	0x45,0x43,0x54,0x52,0x4c,0x3d,0x30,0x2c,0x31,	0x2c,	0x33, 0xd, 0xa};                // AT^TRACECTRL=0,1,3
    //char dev[256];
    char *dev;
	char *cpdev;
	
	char *ATdev;
    printf("%s %s  %d\n", __FILE__, __FUNCTION__,argc);

    // Capture the Ctrl+C
    struct sigaction act;
    act.sa_handler = ctrl_c_process;
    act.sa_flags = 0;
    printf("%s %s  %d\n", __FILE__, __FUNCTION__,argc);
    // signal(SIGTERM, ctrl_c_process);

    if (sigaction(SIGINT, &act, NULL) < 0)
    {
        printf("Install Signal Action Error: %s \n", strerror(errno));
        return 0;
    }
    printf("%s %s  %d\n", __FILE__, __FUNCTION__,argc);
    if (argc == 2 || argc == 3 || argc == 4)
    {
		#if CATCH_CP_LOG

		cpdev = devname(AIRM2M_USB_DEVICE_CP_DIAG_INTERFACE_ID,path_CP,0);
		if(cpdev == NULL)
		{
			ATdev = devname(AIRM2M_USB_DEVICE_AT_PPP_INTERFACE_ID,path0,1);
			fdat = openport(ATdev);
			printf(" open AT PORT1 %s %s  %s\n", __FILE__, __FUNCTION__,ATdev);
			writeport(fdat, OPENCP, 20);
			close(fdat);
			sleep(5);
			ATdev = devname(AIRM2M_USB_DEVICE_AT_PPP_INTERFACE_ID,path0,1);
			fdat = openport(ATdev);
			writeport(fdat, OPENAP, 20);
			sleep(1);
			readport(fdat,pathtest,30);
				
			printf(" read fdat  %s \n", pathtest);
		}

		
		cpdev = devname(AIRM2M_USB_DEVICE_CP_DIAG_INTERFACE_ID,path_CP,1);
		
		#endif

		dev = devname(AIRM2M_USB_DEVICE_AP_DIAG_INTERFACE_ID,path,1);
		
		
    }
    else if (argc == 5)
    {
        dev = argv[4];
    }
	else if (argc == 5)
    {
        dev = argv[4];
		cpdev = argv[5];
    }

    printf("%s %s %s %s %d\n", __FILE__, __FUNCTION__, dev,cpdev,argc);
    // dev = argv[1];

    if (argc == 4 || argc == 5)
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
    else if (argc == 2 || argc == 6)
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
        printf("Opened the device %s fd %d\n", dev,fd);
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
        printf("Can't Open Serial Port fd %d!\n",fd);
        return 0;
    }
#if CATCH_CP_LOG
	fdcp = openport(cpdev);

	if (fdcp >= 0)
		{
			printf("Opened the CP device %s fdcp %d\n", cpdev,fdcp);
			if (strstr(dev, "MDiagUSB") == NULL)
			{
				ret = setport(fdcp, 115200, 8, 1, 'n'); //Set serial port
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
			printf("Can't Open Serial Port fdcp %d!\n",fdcp);
			return 0;
		}
#endif
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
    printf("open port ok.\n");

#if CATCH_CP_LOG
    if (!create_thread(&pppd_thread, cp_thread_function, NULL))
    	{
    		printf("pppd_create_thread succ!");
    	}
    else
        return -1;


	
#endif
    if (!create_thread(&pppd_thread_AP, ap_thread_function, NULL))
    	{
    		printf("pppd_create_thread succ!");
    	}
    else
        return -1;

	

    printf("Sent CMD, receiving data. Press Ctrl+C to exit.\n");
    while (1)
    {
	        // rc = readport0(fd, rbuf, 2000); //Read data, timeout is 500 ms
		sleep(1);

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
