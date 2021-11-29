#ifndef CONTROL_H
#define CONTROL_H

#include "stdbool.h"

typedef struct 
{
    bool lock_state;
    float distance;
}control_t;

extern control_t;

void control_init(void);


#endif