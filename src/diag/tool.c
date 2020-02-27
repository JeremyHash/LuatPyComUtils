#include "tool.h"
#include <dirent.h>
#include <errno.h>
#include <fcntl.h>
#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>
#include <regex.h>

#define EXIT(msg)           \
    do                      \
    {                       \
        perror(msg);        \
        exit(EXIT_FAILURE); \
    } while (0)

#define DECLEARE_DEV(dev)
#define DEFINE_DEV(ifn, name) {":[0-9]\\."#ifn, name}
#define IFN(dev) table[dev][0]
#define NAME(dev) table[dev][1]

const char *table[E_TOTAL][2] = {
    DECLEARE_DEV(E_AT)
    DEFINE_DEV(2, "ttyUSB"),
    DECLEARE_DEV(E_PPP)
    DEFINE_DEV(3, "ttyUSB"),
    DECLEARE_DEV(E_DIAG)
    DEFINE_DEV(4, "ttyUSB"),
    DECLEARE_DEV(E_RNDIS)
    DEFINE_DEV(0, "net")
};

int debug(const char *fmt, ...)
{
#if defined(T_DEBUG)
    int ret;
    va_list ap;
    va_start(ap, fmt);
    printf("debug: ");
    ret = vprintf(fmt, ap);
    va_end(ap);
    return ret;
#else
    return 0;
#endif
}

char *impl(char *name)
{
    static char *stack[10];
    static int i = -1;
    if (name == NULL)
    {
        if (i < 0)
        {
            printf("impl: stack underflow\n");
            exit(EXIT_FAILURE);
        }
        return stack[i--];
    }
    if (++i > 9)
    {
        printf("impl: stack overflow\n");
        exit(EXIT_FAILURE);
    }
    stack[i] = name;
    return stack[i];
}

DIR *Opendir(const char *name)
{
    static char buff[256] = {0};
    DIR *dirp;
    getcwd(buff, 256);
    char *dir = (char *)malloc(strlen(buff) + 1);
    strcpy(dir, buff);
    impl(dir);
    if ((dirp = opendir(name)) == NULL)
        EXIT("opendir");
    if (chdir(name) != 0)
        EXIT("chdir");
    debug("enter folder %s\n", name);
    return dirp;
}

void Closedir(DIR *dirp)
{
    char *dir = impl(NULL);
    debug("leave\n");
    if (chdir(dir) != 0)
        EXIT("chdir");
    if (closedir(dirp) != 0)
        EXIT("closedir");
    free((void *)dir);
}

int ismatched(const char *id, const char *name)
{
    static char buff[5] = {'\0'};
    int fd;
    fd = open(name, O_RDONLY);
    if (fd < 0)
        EXIT("open");
    read(fd, buff, 4);
    debug("%s: %s\n", name, buff);
    if (strcmp(id, buff) == 0)
        return 1;
    return 0;
}

int checkid(DIR *dirp)
{
    static const char *vender = "1286";
    static const char *product = "4e3d";
    int ret = 0;
    int step = 2;
    struct dirent *entp = NULL;
    while ((entp = readdir(dirp)) != NULL)
    {
        if (strcmp("idVendor", entp->d_name) == 0)
        {
            if (ismatched(vender, entp->d_name))
                step--;
        }
        if (strcmp("idProduct", entp->d_name) == 0)
        {
            if (ismatched(product, entp->d_name))
                step--;
        }
        if (!step)
        {
            ret = 1;
            break;
        }
    }
    return ret;
}

char *findent(DIR *dirp, const char *regex)
{
    char *ret = NULL;
    regex_t preg;
    struct dirent *entp = NULL;
    regcomp(&preg, regex, REG_EXTENDED | REG_NOSUB);
    while ((entp = readdir(dirp)) != NULL)
    {
        if (regexec(&preg, entp->d_name, 0, NULL, REG_NOTBOL | REG_NOTEOL) == 0)
        {
            debug("find %s\n", entp->d_name);
            ret = entp->d_name;
            break;
        }
    }
    return ret;
}

char *findif(DIR *dirp, const char *regex, const char *name)
{
    char *ifdir = NULL;
    char *dev = NULL;
    ifdir = findent(dirp, regex);
    if (ifdir != NULL)
    {
        DIR *dp = Opendir(ifdir);
        dev = findent(dp, name);
        if (strcmp(name, "net") == 0 && dev != NULL)
        {
            DIR *net = Opendir(dev);
            dev = findent(net, "eth");
            Closedir(net);
        }
        Closedir(dp);
    }
    return dev;
}

const char *dev_name_impl(const char *regex, const char *name)
{
    char *dev = NULL;
    const char *searchPath = "/sys/bus/usb/devices/";
    DIR *searchDir = Opendir(searchPath);

    struct dirent *entp;
    while ((entp = readdir(searchDir)) != NULL)
    {
        if (entp->d_type == DT_LNK)
        {
            DIR *udirp = Opendir(entp->d_name);
            if (udirp == NULL)
                EXIT("opendir");

            if (checkid(udirp))
            {
                debug("id matched\n");
                rewinddir(udirp);
                dev = findif(udirp, regex, name);
                Closedir(udirp);
                break;
            }
            else
            {
                debug("id dismatch\n");
            }
            Closedir(udirp);
        }
    }

    Closedir(searchDir);
    return dev;
}

const char *dev_name(DEV_E dev)
{
    debug("if %d and name %s\n", IFN(dev), NAME(dev));
    return dev_name_impl(IFN(dev), NAME(dev));
}
