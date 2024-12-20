#include "../gpio_config/gpio_config_io.h"
#include <bitstream.h>
#include <defs.h>
#include <global_defs.h>
#include <helpers.h>
#include <register_actions.h>
#include <stub.h>
#include <upload_bitstream.h>

int main() {
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0;
    reg_gpio_ien = 1;
    reg_gpio_oe = 1;
    reg_gpio_out = 1;
    reg_uart_enable = 1u;

    blink(5, 5000000);
    reg_gpio_out = 1;
    gpio_config_io();
    blink(3, 10000000);

    reg_gpio_out = 0;

    while (1)
        ;

    return 0;
}
