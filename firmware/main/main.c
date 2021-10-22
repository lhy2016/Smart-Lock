/* Hello World Example

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/
#include <stdio.h>
#include "sdkconfig.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "esp_system.h"
#include "esp_spi_flash.h"
#include "driver/i2c.h"
#include "esp_log.h"
#include "driver/gpio.h"
#include "i2c_interface.h"
#include "lcd_display.h"
#include "wifi_hal.h"
#include "tcp_client_hal.h"
#include "pwm.h"
#include "camera.h"
#include "driver/sdmmc_host.h"
#include "sdmmc_cmd.h"

#ifdef CONFIG_IDF_TARGET_ESP32
#define CHIP_NAME "ESP32"
#endif

#ifdef CONFIG_IDF_TARGET_ESP32S2BETA
#define CHIP_NAME "ESP32-S2 Beta"
#endif

#define CAM_MODE  1
#define LOCK_MODE 0

/********************************* Macro Declaration *********************************************/


// Debug Flags
#define I2C_TEST    1
#define COL_START   3
#define COL_END     17
#define ROW_START   1
#define ROW_END     2
#define GPIO_BUTTON 12

/********************************* Structure Declaration *****************************************/








/************************************ Handle Declaration *****************************************/
static TaskHandle_t display_task_handle;
static TaskHandle_t gpio_task_handle;
static TaskHandle_t tcp_task_handle;



extern screen_buffer_t *ph_screen;
extern uint32_t hall_reading[3];

/************************************ Buffer  Declaration ****************************************/


/************************************ Utility Declaration ****************************************/

/************************************ Task Declaration *******************************************/



void LCD_Update_Task()
{
    ESP_LOGI(TAG,"LCD INIT DONE\n");
    while(1)
    {
        if(LCD_update)
        {
            ESP_LOGI(TAG,"draw\n");
            draw();
            LCD_update = false;
        }
        vTaskDelay(100);
    }
}

void GPIO_Check()
{
    gpio_set_direction(GPIO_BUTTON,GPIO_MODE_INPUT);
    gpio_pulldown_en(GPIO_BUTTON);
    ESP_LOGI(TAG,"GPIO DONE\n");
    while(1)
    {
        
        if(gpio_get_level(GPIO_BUTTON) == 1)
        {
            ESP_LOGI(TAG, "GPIO update");
            tcp_payload_update=1;
            pwm_update = !pwm_update;
            LCD_update = true;
        }
        vTaskDelay(100);
    }
}

void app_main(void)
{
    printf("Hello world!\n");

    esp_log_level_set("i2c",ESP_LOG_VERBOSE);    

    i2c_master_init();

    i2c_init_display_sequence();

    lcd_display_init();
 
    wifi_init();

#if LOCK_MODE
    xTaskCreate(LCD_Update_Task,
                "Display loop",
                4096,
                0,
                1,
                &display_task_handle
                );
    

    xTaskCreate(mcpwm_example_servo_control, 
                "mcpwm_example_servo_control", 
                4096, 
                NULL, 
                5, 
                NULL);
#endif         

xTaskCreate(tcp_client_task,
                "TCP client packet",
                8000,
                0,
                5,
                &tcp_task_handle
                );

xTaskCreate(GPIO_Check,
                "GPIO check task",
                4096,
                0,
                3,
                &gpio_task_handle
                ); 

#if CAM_MODE
    
    ESP_LOGI(TAG,"CAM REGISTER\n");
    xTaskCreate(take_picture, 
                "cam_module", 
                16384, 
                NULL, 
                5, 
                NULL);
#endif

}
