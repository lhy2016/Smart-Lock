/**
 * This example takes a picture every 5s and print its size on serial monitor.
 */

// =============================== SETUP ======================================

// 1. Board setup (Uncomment):
// #define BOARD_WROVER_KIT
// #define BOARD_ESP32CAM_AITHINKER

/**
 * 2. Kconfig setup
 * 
 * If you have a Kconfig file, copy the content from
 *  https://github.com/espressif/esp32-camera/blob/master/Kconfig into it.
 * In case you haven't, copy and paste this Kconfig file inside the src directory.
 * This Kconfig file has definitions that allows more control over the camera and
 * how it will be initialized.
 */

/**
 * 3. Enable PSRAM on sdkconfig:
 * 
 * CONFIG_ESP32_SPIRAM_SUPPORT=y
 * 
 * More info on
 * https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/kconfig.html#config-esp32-spiram-support
 */

// ================================ CODE ======================================

#include "camera.h"
#include "lcd_display.h"
#include "driver/gpio.h"
#include "sdmmc_cmd.h"
#include "driver/sdmmc_types.h"
#include "driver/sdmmc_host.h"

#define FLASH_LED 4

static esp_err_t init_camera()
{
    //initialize the camera
    esp_err_t err = esp_camera_init(&camera_config);
    if (err != ESP_OK)
    {
        ESP_LOGE(TAG, "Camera Init Failed");
        return err;
    }

    return ESP_OK;
}

void take_picture()
{
    if(ESP_OK != init_camera()) {
        
        ESP_LOGI(TAG,"CAMERA INIT FAIL DONE\n");
        return;
    }

    gpio_set_direction(FLASH_LED,GPIO_MODE_OUTPUT);
    gpio_pulldown_en(FLASH_LED);

    while (1)
    {
        if(LCD_update)
        {
        ESP_LOGI(TAG, "Taking picture...");
        
        gpio_set_level(FLASH_LED,1);

        pic = esp_camera_fb_get();

        gpio_set_level(FLASH_LED,0);
            
        // use pic->buf to access the image
        ESP_LOGI(TAG, "Picture taken! Its size was: %zu bytes", pic->len);
        ESP_LOGI(TAG, "\nPicture taken! Its width was: %zu bytes", pic->width);
        esp_camera_fb_return(pic);
        printf("smt\n");




        vTaskDelay(5000 / portTICK_RATE_MS);
        LCD_update = false;
        }
    }
}
