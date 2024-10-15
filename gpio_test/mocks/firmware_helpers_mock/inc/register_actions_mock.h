#pragma once
#define FFF_GCC_FUNCTION_ATTRIBUTES __attribute__((weak))
#include <fff.h>
#include <register_actions.h>

DECLARE_FAKE_VOID_FUNC(set_bit, uint8_t, volatile uint32_t *const);
DECLARE_FAKE_VOID_FUNC(clear_bit, uint8_t, volatile uint32_t *const);
DECLARE_FAKE_VOID_FUNC(set_or_clear_bit, uint8_t, volatile uint32_t *const,
                       bool);
