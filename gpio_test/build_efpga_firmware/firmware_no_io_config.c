#include <bitstream.h>
#include <defs.h>
#include <global_defs.h>
#include <helpers.h>
#include <register_actions.h>
#include <stub.h>

// Do not configure the IOs here to be able to always upload
// a bitstream (although the outputs will never work)

int main() {
    reg_gpio_mode1 = 1;
    reg_gpio_mode0 = 0;
    reg_gpio_ien = 1;
    reg_gpio_oe = 1;
    reg_gpio_out = 1;

    reg_gpio_out = 1;

    blink(3, 2500000);
    reg_gpio_out = 0;

    while (1) {
    }

    return 0;
}
