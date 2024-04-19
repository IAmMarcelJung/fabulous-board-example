#pragma once
#define FFF_GCC_FUNCTION_ATTRIBUTES __attribute__((weak))
#include <io_def.h>
#include <fff.h>

DECLARE_FAKE_VOID_FUNC(set_pin, uint8_t, te_chain);
DECLARE_FAKE_VOID_FUNC(clear_pin, uint8_t, te_chain);
DECLARE_FAKE_VOID_FUNC(set_or_clear_pin, uint8_t, te_chain, bool);

void my_fake(uint8_t arg0, te_chain channel, bool set);
