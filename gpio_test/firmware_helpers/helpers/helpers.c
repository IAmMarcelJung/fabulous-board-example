#include "helpers.h"
#include "../gpio_config/gpio_config_io.h"
#include <global_defs.h>
#include <register_actions.h>
#include <stub.h>
/**
 * @brief Let the LED connected to the single gpio pin blink.
 * @param cylces: The number of cycles the LED will blink.
 * @param interval: The interval in which the LED will blink.
 * This is effectively the delay in clock cylces between the on and off state.
 */
void blink(uint32_t toggles, uint32_t interval) {
  uint32_t old = reg_gpio_out & 1u;
  for (uint32_t i = 0u; i < toggles * 2; i++) {
    set_or_clear_bit(REGISTER_0_DATA_BIT_POS, &reg_gpio_out, (bool)old);
    old = ~old & 1u;
    delay(interval);
  }
}

/**
 * @brief Print a word over UART.
 * @param word: The word to be printed.
 */
void print_word(uint32_t word) {
  for (uint8_t byte = 0u; byte < BYTES_IN_WORD; byte++) {
    char current_byte =
        (word >> ((BYTES_IN_WORD - 1u - byte) * BITS_IN_BYTE)) & 0xFF;
    uart_putchar(current_byte);
  }
}
