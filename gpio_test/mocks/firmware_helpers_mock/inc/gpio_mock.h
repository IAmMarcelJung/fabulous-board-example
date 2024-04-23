#pragma once
#define FFF_GCC_FUNCTION_ATTRIBUTES __attribute__((weak))
#include <gpio.h>
#include <fff.h>

DECLARE_FAKE_VOID_FUNC(set_gpio, uint8_t);
DECLARE_FAKE_VOID_FUNC(clear_gpio, uint8_t);
DECLARE_FAKE_VOID_FUNC(set_or_clear_gpio, uint8_t, bool);

void write_bit_to_file(uint8_t pin, bool set);
