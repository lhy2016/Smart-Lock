#ifndef LCD_DISPLAY
#define LCD_DISPLAY

/************************************* Structure declaration *************************************/
#include "stdint.h"
#include "stdbool.h"

extern uint8_t ascii_decoder[256][6];
bool LCD_update;

typedef struct
{
    uint8_t pixels[6];
}character_t;

typedef struct 
{
    character_t characters[21];
}rows_t;

typedef struct 
{
    rows_t rows[4];
}screen_t;

typedef union 
{
    screen_t screen;
    uint8_t screen_buffer[504];
    character_t character_buffer[84];
}screen_buffer_t;

typedef union
{
    character_t ASCII_table[128];
    uint8_t ASCII_buffer[896];
}ascii_table_t;

typedef enum
{
    DOOR_STATE = 0,
    TCP_RX_DATA,
    TOTAL_DISPLAY_ITEM,
}display_layout_enum_t;

typedef struct 
{
    uint32_t start_addr;
    uint32_t size;
}lcd_display_item_t;


typedef struct 
{
    lcd_display_item_t item[TOTAL_DISPLAY_ITEM];
}lcd_display_arrangement_t;



extern lcd_display_arrangement_t *lcd_layout;
extern screen_buffer_t *ph_screen;


void draw();

void draw_char(int x, int col, char c);

void lcd_display_init();

void draw_area(uint8_t cs, uint8_t ce, uint8_t rs, uint8_t re);

void update_item(display_layout_enum_t item_id, char *x);




#endif
