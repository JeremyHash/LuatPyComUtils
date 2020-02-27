#ifndef _TOOL_H_
#define _TOOL_H_

// #define T_DEBUG

typedef enum
{
    E_AT,
    E_PPP,
    E_DIAG,
    E_RNDIS,
    E_TOTAL
} DEV_E;

const char *dev_name(DEV_E dev);

#endif
