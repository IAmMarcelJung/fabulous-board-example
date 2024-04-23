#include <stdint.h>
#include <defs.h>

#include <register_actions.h>
#include <global_defs.h>
#include <gpio.h>

/**
 * @brief Set the given pin.
 * @param pin The pin to be set.
 */
void set_pin(uint8_t pin)
{
    if (BITS_IN_WORD > pin)
    {
        set_bit(pin, &reg_mprj_datal);
    }
    else
    {
        pin -= BITS_IN_WORD;
        set_bit(pin, &reg_mprj_datah);
    }
}

/**
 * @brief Clear the given pin.
 * @param pin The pin to be cleared.
 */
void clear_pin(uint8_t pin)
{
    if (BITS_IN_WORD > pin)
    {
        clear_bit(pin, &reg_mprj_datal);
    }
    else
    {
        pin -= BITS_IN_WORD;
        clear_bit(pin, &reg_mprj_datah);
    }
}

/**
 * @brief Set or clear the given pin.
 * @param pin The pin to be set or cleared.
 * @param set A flag to select whether to set or clear the pin.
 */
void set_or_clear_pin(uint8_t pin, bool set)
{
    if (true == set)
    {
        set_pin(pin);
    }
    else
    {
        clear_pin(pin);
    }
}
