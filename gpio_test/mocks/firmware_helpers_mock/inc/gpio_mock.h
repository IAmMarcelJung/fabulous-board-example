#pragma once
#define FFF_GCC_FUNCTION_ATTRIBUTES __attribute__((weak))
#include <fff.h>
#include <gpio.h>

DECLARE_FAKE_VOID_FUNC(gpio_init, GPIO *const);
DECLARE_FAKE_VOID_FUNC(set_gpio, uint8_t);
DECLARE_FAKE_VOID_FUNC(clear_gpio, uint8_t);
DECLARE_FAKE_VOID_FUNC(set_or_clear_gpio, uint8_t, bool);

void write_bit_to_file(uint8_t pin, bool set);
void write_newline_to_file(uint8_t pin);
