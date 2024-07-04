#include <register_actions_mock.h>

DEFINE_FAKE_VOID_FUNC(set_bit, uint8_t, volatile uint32_t * const);                    
DEFINE_FAKE_VOID_FUNC(clear_bit, uint8_t, volatile uint32_t * const);                    
DEFINE_FAKE_VOID_FUNC(set_or_clear_bit, uint8_t, volatile uint32_t * const, bool);                    
