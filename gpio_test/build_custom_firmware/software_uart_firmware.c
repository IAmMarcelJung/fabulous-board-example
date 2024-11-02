#include "../gpio_config/gpio_config_io.h"
#include <bitstream.h>
#include <helpers.h>
#include <software_uart.h>

int main() {

    uart_config_t uart_config = {.baud_rate = BAUD_RATE_MPW_5, .parity = ODD};
    software_uart_init(&uart_config);
    uint32_t bitstream_size = sizeof(bitstream) / sizeof(uint8_t);
    for (uint32_t byte_pos = 0u; byte_pos < bitstream_size; byte_pos++) {
        uint8_t byte = bitstream[byte_pos];
        software_uart_tx_byte(byte);
        // TODO: test how long to wait between two frames
        delay(100);
    }

    reg_gpio_out = 0;

    gpio_config_io();

    while (1)
        ;

    return 0;
}
