#pragma once
#define FFF_GCC_FUNCTION_ATTRIBUTES __attribute__((weak))
#include <fff.h>
#include <upload_bitstream.h>

DECLARE_FAKE_VOID_FUNC(upload_bitstream, uint8_t const *const, uint32_t);
