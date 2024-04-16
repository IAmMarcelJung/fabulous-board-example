#include <stdint.h>

#include "../riscv_firmware_src/defs.h"
#include "io_def.h"

/**
 * @brief Set the given pin of the given chain.
 * @param pin The pin to be set.
 * @param chain The GPIO chain to be used.
 */ 
void set_pin(uint8_t pin, te_chain chain)
{
    if (LOW_CHAIN == chain)
    {
        reg_mprj_datal |= IO_DATA_BIT(pin);
    }
    else
    {
        reg_mprj_datah |= IO_DATA_BIT(pin);
    }
}

/**
 * @brief Clear the given pin of the given chain.
 * @param pin The pin to be cleared.
 * @param chain The GPIO chain to be used.
 */ 
void clear_pin(uint8_t pin, te_chain chain)
{
    if (LOW_CHAIN == chain)
    {
        reg_mprj_datal &= ~(IO_DATA_BIT(pin));
    }
    else
    {
        reg_mprj_datah &= ~(IO_DATA_BIT(pin));
    }
}

/**
 * @brief Set or clear the given pin of the given chain depending on a flag.
 * @param pin The pin to be set or cleared.
 * @param chain The GPIO chain to be used.
 * @param set A flag to select whether to set or clear the pin.
 */ 
void set_or_clear_pin(uint8_t pin, te_chain chain, bool_t set)
{
    if (true == set) 
    {
        set_pin(pin, chain);
    }
    else
    {
        clear_pin(pin, chain);
    }
}
