/**
 * @file i2c_interface.h
 * @author your name (you@domain.com)
 * @brief 
 * @version 0.1
 * @date 2021-06-17
 * 
 * @copyright Copyright (c) 2021
 * 
 */
#ifndef I2C_INTERFACE_H
#define I2C_INTERFACE_H


#define POS_I2C_INIT_READ                   (0x79)      // I2C SAD+
#define ANG_I2C_INIT_READ                   (0x3D)
#define POS_I2C_INIT_WRITE                  (0x78) 
#define ANG_I2C_INIT_WRITE                  (0x3C)
#define ACK_CHECK_EN   0x1     /*!< I2C master will check ack from slave*/
#define ACK_CHECK_DIS  0x0     /*!< I2C master will not check ack from slave */
#define ACK_VAL    0x0         /*!< I2C ack value */
#define NACK_VAL   0x1         /*!< I2C nack value */

#include "stdint.h"
/**
 * @brief 
 * 
 * @return uint32_t 
 */
uint32_t i2c_master_init();

/**
 * @brief 
 * 
 * @param data 
 * @return uint32_t 
 */
uint32_t i2c_send_cmd(uint8_t data);

/**
 * @brief 
 * 
 * @param data 
 * @return uint32_t 
 */
uint32_t i2c_send_data(uint8_t data);

/**
 * @brief 
 * 
 */
void i2c_init_display_sequence();


#endif /* I2C_INTERFACE */
