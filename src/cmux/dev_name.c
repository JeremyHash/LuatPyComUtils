#include "tool.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

char path[256] = "/dev/";

const char *devname(DEV_E dev)
{
    const char *name = dev_name(dev);
    if (name == NULL)
    {
        switch (dev)
        {
        case E_AT:
            fprintf(stderr, "can not find at port\n");
            break;
        case E_DIAG:
            fprintf(stderr, "can not find diag port\n");
            break;
        case E_PPP:
            fprintf(stderr, "can not find ppp port\n");
            break;
        case E_RNDIS:
            fprintf(stderr, "can not find rndis netcard\n");
            break;
        }
        exit(EXIT_FAILURE);
    }
    if (dev == E_RNDIS)
    {
        return name;
    }
    strcat(path, name);
    return path;
}

int main(int argc, char **argv)
{
    if (argc != 2)
    {
        fprintf(stderr, "./dev_name at|ppp|diag|rndis\n");
        return -1;
    }

    if (strcmp("at", argv[1]) == 0)
    {
        printf("%s\n", devname(E_AT));
        return 0;
    }

    if (strcmp("ppp", argv[1]) == 0)
    {
        printf("%s\n", devname(E_PPP));
        return 0;
    }

    if (strcmp("diag", argv[1]) == 0)
    {
        printf("%s\n", devname(E_DIAG));
        return 0;
    }

    if (strcmp("rndis", argv[1]) == 0)
    {
        printf("%s\n", devname(E_RNDIS));
        return 0;
    }
}