#include "control.h"

control_t control;

void control_init()
{
    control.distance = 0;
    control.lock_state = true;
}