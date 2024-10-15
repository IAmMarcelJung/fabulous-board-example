#include <gpio_config_io_mock.h>

DEFINE_FAKE_VOID_FUNC(delay, const int);
DEFINE_FAKE_VOID_FUNC(bb_mode);
DEFINE_FAKE_VOID_FUNC(load);
DEFINE_FAKE_VOID_FUNC(clear_registers);
DEFINE_FAKE_VOID_FUNC(gpio_config_io);
