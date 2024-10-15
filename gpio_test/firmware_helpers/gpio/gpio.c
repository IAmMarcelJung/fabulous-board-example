#include <defs.h>
#include <stdint.h>

#include <global_defs.h>
#include <gpio.h>
#include <register_actions.h>

typedef void (*BitOpFunctionPointer)(uint8_t, volatile uint32_t *);

static void execute_bit_op_for_gpio(uint8_t pin,
                                    BitOpFunctionPointer bit_op_ptr);

static volatile uint32_t reg_mprj_datal_shadow = 0u;
static volatile uint32_t reg_mprj_datah_shadow = 0u;
static GPIO *gpio_internal;

/**
 * @brief Initialize the GPIO module by specifing the pointers to the registers.
 * @remark This functionality is needed to access the value when testing.
 * @param gpio The pointer be set for the gpio instance.
 */
void gpio_init(GPIO *const gpio) { gpio_internal = gpio; }

/**
 * @brief Set the given pin.
 * @param pin The pin to be set.
 */
void set_gpio(uint8_t pin) { execute_bit_op_for_gpio(pin, &set_bit); }

/**
 * @brief Clear the given pin.
 * @param pin The pin to be cleared.
 */
void clear_gpio(uint8_t pin) { execute_bit_op_for_gpio(pin, &clear_bit); }

/**
 * @brief Set or clear the given pin.
 * @param pin The pin to be set or cleared.
 * @param set A flag to select whether to set or clear the pin.
 */
void set_or_clear_gpio(uint8_t pin, bool set) {
    if (true == set) {
        execute_bit_op_for_gpio(pin, &set_bit);
    } else {
        execute_bit_op_for_gpio(pin, &clear_bit);
    }
}

/**
 * @brief Execute a given bit operation for a given pin.
 * @param pin The pin to execute the function for.
 * @param The bit operation to execute for the pin.
 */
static void execute_bit_op_for_gpio(uint8_t pin,
                                    BitOpFunctionPointer bit_operation) {
    if (BITS_IN_WORD > pin) {
        bit_operation(pin, &reg_mprj_datal_shadow);
        *(gpio_internal->datal_reg_pointer) = reg_mprj_datal_shadow;
    } else {
        pin -= BITS_IN_WORD;
        bit_operation(pin, &reg_mprj_datah_shadow);
        *(gpio_internal->datah_reg_pointer) = reg_mprj_datah_shadow;
    }
}
