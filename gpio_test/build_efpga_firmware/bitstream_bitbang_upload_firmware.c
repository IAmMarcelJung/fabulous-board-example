#include "../gpio_config/gpio_config_io.h"
#include <bitstream.h>
#include <gpio_config_data.h>
#include <helpers.h>
#include <upload_bitstream.h>

int main() {
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0;
    reg_gpio_ien = 1;
    reg_gpio_oe = 1;
    reg_gpio_out = 1;

    blink(3, 5000000);
    reg_gpio_out = 1;
    gpio_config_io(config_stream);

    blink(3, 5000000);
    reg_gpio_out = 1;

    GPIO gpio;
    gpio.datah_reg_pointer = &reg_mprj_datah;
    gpio.datal_reg_pointer = &reg_mprj_datal;

    bitstream_init(&gpio);

    upload_bitstream((uint8_t *)&bitstream,
                     sizeof(bitstream) / sizeof(uint8_t));

    blink(3, 5000000);
    reg_gpio_out = 0;
    while (1)
        ;

    return 0;
}
