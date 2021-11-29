#include "i2c_interface.h"
#include "driver/i2c.h"

uint32_t i2c_master_init(void)
{
    int i2c_master_port = 0;
    i2c_config_t conf;
    conf.mode = I2C_MODE_MASTER;
    conf.sda_io_num = 21;
    conf.sda_pullup_en = GPIO_PULLUP_ENABLE;
    conf.scl_io_num = 22;
    conf.scl_pullup_en = GPIO_PULLUP_ENABLE;
    conf.master.clk_speed = 50000;
    i2c_param_config(0, &conf);
    return (uint32_t)i2c_driver_install(i2c_master_port, conf.mode, 0, 0, 0);
}

uint32_t i2c_send_cmd(uint8_t data)
{
    uint32_t err = 0;
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    err |= i2c_master_write_byte(cmd,0x78,ACK_CHECK_EN);
    err |= i2c_master_write_byte(cmd,0x80,ACK_CHECK_EN);
    err |= i2c_master_write_byte(cmd,data,ACK_CHECK_EN);
    i2c_master_stop(cmd);
    err = i2c_master_cmd_begin(0,cmd,1000/portTICK_RATE_MS);
    i2c_cmd_link_delete(cmd);
    return err;
}

uint32_t i2c_send_data(uint8_t data)
{
    uint32_t err = 0;
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    err |= i2c_master_write_byte(cmd,0x78,ACK_CHECK_EN);
    err |= i2c_master_write_byte(cmd,0x40,ACK_CHECK_EN);
    err |= i2c_master_write_byte(cmd,data,ACK_CHECK_EN);
    i2c_master_stop(cmd);
    err = i2c_master_cmd_begin(0,cmd,1000/portTICK_RATE_MS);
    i2c_cmd_link_delete(cmd);
    return err;
}

void i2c_init_display_sequence()
{
    uint8_t init_seq[27] = {0xAE,0xD5,0xF0,0xA8,0x1F,0xD3,0x00,0x40,0x8D,0x14,0x20,0x00,0xA0,0xC0,0xDA,0x02,0x81,0x18,0xA5,0xD9,0xF1,0xDB,0x40,0xA4,0xA6,0x2E,0xAF};
    for(int i = 0; i < 27; i++)
    {
        i2c_send_cmd(init_seq[i]);
    }
}

