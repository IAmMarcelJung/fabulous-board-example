#include "software_uart.h"
#include <defs.h>
#include <gpio_config_io.h>

#define BITS_IN_BYTE 8u

#define UART_FRAME_SIZE 11u

#define START_BIT 0u
#define STOP_BIT 1u

#define START_BIT_POS 0u
#define PARITY_BIT_POS 9u
#define STOP_BIT_POS 10u

#define EVEN_PARITY 0u;
#define ODD_PARITY 1u;

#define UART_IDLE_STATE 1u

uart_config_t uart_config = {.baud_rate = BAUD_RATE_MPW_5, .parity = ODD};
uint32_t bit_time = CPU_FREQ / BAUD_RATE_MPW_5;

static void byte_to_bits(uint8_t const byte, uint8_t *const frame);

void software_uart_init(uart_config_t const *const config) {
    uart_config.baud_rate = config->baud_rate;
    uart_config.parity = config->parity;
    int32_t cpu_frequency = CPU_FREQ;
    bit_time = 0u;
    while (cpu_frequency >= config->baud_rate) {
        cpu_frequency -= config->baud_rate;
        bit_time++;
    }
    reg_gpio_mode1 = 1u;
    reg_gpio_mode0 = 0u;
    reg_gpio_ien = 1u;
    reg_gpio_oe = 1u;

    reg_gpio_out = UART_IDLE_STATE;
}

void software_uart_tx_byte(uint8_t const byte) {
    uint8_t frame[UART_FRAME_SIZE];
    frame[START_BIT_POS] = START_BIT;
    frame[STOP_BIT_POS] = STOP_BIT;
    byte_to_bits(byte, frame);
}

static void byte_to_bits(uint8_t const byte, uint8_t *const frame) {
    uint8_t bit;
    uint8_t parity;
    if (uart_config.parity == EVEN) {
        parity = 0u;
    } else {
        parity = 1u;
    }

    // LSB to MSB
    for (uint8_t bit_pos = 1u; bit_pos <= BITS_IN_BYTE; bit_pos++) {
        bit = byte >> (bit_pos - 1u) & 0x1u;
        frame[bit_pos] = bit;
        if (bit != 0u) {
            parity = ~parity;
        }
    }
    frame[PARITY_BIT_POS] = parity;
}

static void transfer_frame(uint8_t const *const frame) {
    for (uint8_t bit_pos = 0u; bit_pos < UART_FRAME_SIZE; bit_pos++) {
        reg_gpio_out = frame[bit_pos];
        delay(bit_time);
    }
    reg_gpio_out = UART_IDLE_STATE;
}
