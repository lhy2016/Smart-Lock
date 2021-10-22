/**
 * @file wifi_hal.h
 * @author your name (you@domain.com)
 * @brief 
 * @version 0.1
 * @date 2021-09-14
 * 
 * @copyright Copyright (c) 2021
 * 
 */

#ifndef WIFI_HAL_H
#define WIFI_HAL_H

#define WIFI_NAME   "481patricia"
#define WIFI_PASS   "PoisonlessPeachGarden@*8*"
#define DEVICE_ID   0x0000


void wifi_init();

void wifi_connect_handler();

void wifi_disconnect_handler();

#endif