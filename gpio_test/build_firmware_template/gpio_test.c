#include "../riscv_firmware_src/defs.h"
#include "../gpio_config/gpio_config_io.h"

// --------------------------------------------------------
// Firmware routines
// --------------------------------------------------------

int main()
{
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0;
    reg_gpio_ien = 1;
    reg_gpio_oe = 1;
    reg_gpio_out = 1; // OFF

    gpio_config_io();

    reg_gpio_out = 1; // ON

}
