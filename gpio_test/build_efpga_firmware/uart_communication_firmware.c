#include "../gpio_config/gpio_config_io.h"
#include <bitstream.h>
#include <defs.h>
#include <global_defs.h>
#include <helpers.h>
#include <register_actions.h>
#include <stub.h>
#include <upload_bitstream.h>

#define PREAMBLE_SIZE 128u

// --------------------------------------------------------
// Firmware routines
// --------------------------------------------------------
//

void print_gpio_values_header() {
    print("\r");
    char d0 = '0';
    char d1 = '0';

    // HEADER
    for (int32_t i = 0; i < 38; i++) {
        print("[");
        uart_putchar(d1);
        uart_putchar(d0);
        print("] ");
        d0 = d0 + 1;
        if (d0 > ('0' + 9)) {
            d0 = '0';
            d1 = d1 + 1;
        }
    }

    print("\n");
}

char UART_readChar() {
    while (uart_rxempty_read() == 1)
        ;
    uart_ev_pending_write(2);
    return reg_uart_data;
}

void print_gpio_values() {
    // VALUES
    for (int32_t i = 0; i < 38; i++) {
        uint32_t value;

        if (i < 32) {
            value = ((reg_mprj_datal >> i) & 0x1);
        } else {
            value = ((reg_mprj_datah >> (i - 32)) & 0x1);
        }

        print("  ");
        if (value) {
            print("1");
        } else {
            print("0");
        }
        print("  ");
    }
    print("\r");
}
char *UART_readLine() {
    char *received_array = 0;
    char received_char;
    int count = 0;
    while ((received_char = UART_readChar()) != 0x0D) {
        received_array[count++] = received_char;
    }
    received_array[count++] = received_char;
    return received_array;
}

int main() {
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0;
    reg_gpio_ien = 1;
    reg_gpio_oe = 1;
    reg_gpio_out = 1;
    reg_uart_enable = 1u;

    blink(3, 2500000);
    reg_gpio_out = 1;
    gpio_config_io();
    blink(3, 2500000);
    reg_gpio_out = 0;

    while (1) {
        print("Please enter a character:\n");
        // print_gpio_values_header();
        // print_gpio_values();
        // print("\033[A");
        char test = UART_readChar();
        print("The character was: ");
        uart_putchar(test);
        uart_putchar('\n');
    }
    return 0;
}
