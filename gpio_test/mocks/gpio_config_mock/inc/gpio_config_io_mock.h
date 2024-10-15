#pragma once
#define FFF_GCC_FUNCTION_ATTRIBUTES __attribute__((weak))
#include <fff.h>
#include <gpio_config_io.h>

DECLARE_FAKE_VOID_FUNC(delay, const int);
DECLARE_FAKE_VOID_FUNC(bb_mode);
DECLARE_FAKE_VOID_FUNC(load);
DECLARE_FAKE_VOID_FUNC(clear_registers);
DECLARE_FAKE_VOID_FUNC(gpio_config_io);
