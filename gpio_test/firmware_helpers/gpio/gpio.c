#include <stdint.h>
#include <defs.h>

#include <register_actions.h>
#include <global_defs.h>
#include <gpio.h>

typedef void (*BitOpFunctionPointer)(uint8_t, volatile uint32_t *);

void execute_bit_op_for_gpio(uint8_t pin, BitOpFunctionPointer bit_op_ptr);

/**
 * @brief Set the given pin.
 * @param pin The pin to be set.
 */
void set_gpio(uint8_t pin)
{
    execute_bit_op_for_gpio(pin, &set_bit);
}

/**
 * @brief Clear the given pin.
 * @param pin The pin to be cleared.
 */
void clear_gpio(uint8_t pin)
{
    execute_bit_op_for_gpio(pin, &clear_bit);
}

/**
 * @brief Set or clear the given pin.
 * @param pin The pin to be set or cleared.
 * @param set A flag to select whether to set or clear the pin.
 */
void set_or_clear_gpio(uint8_t pin, bool set)
{
    if (true == set)
    {
        execute_bit_op_for_gpio(pin, &set_bit);
    }
    else
    {
        execute_bit_op_for_gpio(pin, &clear_bit);
    }
}

/**
 * @brief Execute a given bit operation for a given pin.
 * @param pin The pin to execute the function for.
 * @param The bit operation to execute for the pin.
 */
void execute_bit_op_for_gpio(uint8_t pin, BitOpFunctionPointer bit_operation)
{
    if (BITS_IN_WORD > pin)
    {
        bit_operation(pin, &reg_mprj_datal);
    }
    else
    {
        pin -= BITS_IN_WORD;
        bit_operation(pin, &reg_mprj_datah);
    }
}
