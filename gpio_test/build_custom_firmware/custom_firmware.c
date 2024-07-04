#include <defs.h>
#include "../gpio_config/gpio_config_io.h"
#include <upload_bitstream.h>
#include <bitstream.h>
#include <register_actions.h>
#include <global_defs.h>
#include <stub.h>

#define PREAMBLE_SIZE 128u

// --------------------------------------------------------
// Firmware routines
// --------------------------------------------------------
//
/**
 * @brief Let the LED connected to the single gpio pin blink.
 * @param cylces: The number of cycles the LED will blink.
 * @param interval: The interval in which the LED will blink.
 * This is effectively the delay in clock cylces between the on and off state.
 */
void blink(uint32_t cylces, uint32_t interval)
{
    uint32_t old = reg_gpio_out & 1u;
    for (uint32_t i = 0u; i < cylces; i++)
    {
        set_or_clear_bit(REGISTER_0_DATA_BIT_POS, &reg_gpio_out, (bool)old);
        old = ~old & 1u;
        delay(interval);
    }
}

/**
 * @brief Print a word over UART.
 * @param word: The word to be printed.
 */
void print_word(uint32_t word)
{
    for (uint8_t byte = 0u; byte < BYTES_IN_WORD; byte++)
    {
        char current_byte = (word >> ((BYTES_IN_WORD - 1u - byte) * BITS_IN_BYTE)) & 0xFF;
        putchar(current_byte);
    }
}

void set_registers() {

    reg_mprj_io_1 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_2 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    reg_mprj_io_3 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    reg_mprj_io_4 = GPIO_MODE_MGMT_STD_INPUT_NOPULL;
    reg_mprj_io_5 = GPIO_MODE_MGMT_STD_INPUT_NOPULL; // Rx
    reg_mprj_io_6 = GPIO_MODE_MGMT_STD_OUTPUT; // Tx
    reg_mprj_io_7 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_8 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_9 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_10 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_11 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_12 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_13 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_14 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_15 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_16 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_17 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_18 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_19 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_20 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_21 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_22 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_23 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_24 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_25 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_26 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_27 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_28 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_29 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_30 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_31 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_32 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_33 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_33 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_34 = GPIO_MODE_USER_STD_BIDIRECTIONAL;
    reg_mprj_io_35 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_36 = GPIO_MODE_MGMT_STD_OUTPUT;
    reg_mprj_io_37 = GPIO_MODE_MGMT_STD_OUTPUT;

}

int main() {
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0;
    reg_gpio_ien = 1;
    reg_gpio_oe = 1;
    reg_gpio_out = 1;
    reg_uart_enable = 1u;

    blink(5, 5000000);
    reg_gpio_out = 1;
    set_registers();
    gpio_config_io();
    blink(3, 10000000);

    print("A");
    delay(500000);
    print("A");
    blink(5, 5000000);
    reg_gpio_out = 1;

    GPIO gpio;
    gpio.datah_reg_pointer = &reg_mprj_datah;
    gpio.datal_reg_pointer = &reg_mprj_datal;

    bitstream_init(&gpio);

    upload_bitstream((uint8_t *)&bitstream, sizeof(bitstream)/sizeof(uint8_t));

    blink(5, 5000000);
    reg_gpio_out = 0;
    while(1);

    return 0;
}
