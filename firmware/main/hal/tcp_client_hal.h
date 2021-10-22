/**
 * @file tcp_client_hal.h
 * @author your name (you@domain.com)
 * @brief 
 * @version 0.1
 * @date 2021-09-14
 * 
 * @copyright Copyright (c) 2021
 * 
 */

#ifndef TCP_CLIENT_HAL_H
#define TCP_CLIENT_HAL_H

#include "stdbool.h"
//#include "freertos/semphr.h"

bool tcp_payload_update;
//extern SemaphoreHandle_t display_buffer_sem;


void tcp_client_task(void *pvParameters);


#endif