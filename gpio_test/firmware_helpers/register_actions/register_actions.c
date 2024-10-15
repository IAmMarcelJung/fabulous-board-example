#include <stdint.h>

#include <register_actions.h>

/**
 * @brief Set the given bit of the given register.
 * @param pin The bit to be set.
 * @param chain The register where to set the bit.
 */
inline void set_bit(uint8_t bit, volatile uint32_t *const reg) {
    *reg |= REGISTER_DATA_BIT(bit);
}

/**
 * @brief Clear the given bit of the given register.
 * @param pin The bit to be cleared.
 * @param chain The reg wheret to clear the bit.
 */
inline void clear_bit(uint8_t bit, volatile uint32_t *const reg) {
    *reg &= ~(REGISTER_DATA_BIT(bit));
}

/**
 * @brief Set or clear the given pin of the given chain depending on a flag.
 * @param pin The pin to be set or cleared.
 * @param chain The GPIO chain to be used.
 * @param set A flag to select whether to set or clear the pin.
 */
inline void set_or_clear_bit(uint8_t bit, volatile uint32_t *const reg,
                             bool set) {
    if (true == set) {
        set_bit(bit, reg);
    } else {
        clear_bit(bit, reg);
    }
}
