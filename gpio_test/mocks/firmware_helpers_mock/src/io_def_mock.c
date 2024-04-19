#include <io_def_mock.h>

DEFINE_FAKE_VOID_FUNC(set_pin, uint8_t, te_chain);
DEFINE_FAKE_VOID_FUNC(clear_pin, uint8_t, te_chain);
DEFINE_FAKE_VOID_FUNC(set_or_clear_pin, uint8_t, te_chain, bool);
