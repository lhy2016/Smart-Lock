#ifndef PWM_H
#define PWM_H

#include "freertos/semphr.h"
#include "stdint.h"

#define GPIO_PWM0A_OUT 19   //Set GPIO 19 as PWM0A
#define GPIO_PWM0B_OUT 18   //Set GPIO 18 as PWM0B
#define GPIO_PWM1A_OUT 17   //Set GPIO 17 as PWM1A
#define GPIO_PWM1B_OUT 16   //Set GPIO 16 as PWM1B
#define GPIO_PWM2A_OUT 15   //Set GPIO 15 as PWM2A
#define GPIO_PWM2B_OUT 14   //Set GPIO 14 as PWM2B
#define GPIO_CAP0_IN   25   //Set GPIO 25 as  CAP0
#define GPIO_CAP1_IN   26   //Set GPIO 26 as  CAP1
#define GPIO_CAP2_IN   27   //Set GPIO 27 as  CAP2

extern uint32_t hall_reading[3];
bool pwm_update;
extern SemaphoreHandle_t display_buffer_sem;

void pwm_init();

void mcpwm_example_servo_control(void *arg);




#endif
