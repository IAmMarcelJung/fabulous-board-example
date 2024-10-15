#ifndef GPIO_H
#define GPIO_H

#include <stdbool.h>
#include <stdint.h>

// Definitons for the GPIO pins
#define GPIO_0 0u
#define GPIO_1 1u
#define GPIO_2 2u
#define GPIO_3 3u
#define GPIO_4 4u
#define GPIO_5 5u
#define GPIO_6 6u
#define GPIO_7 7u
#define GPIO_8 8u
#define GPIO_9 9u
#define GPIO_10 10u
#define GPIO_11 11u
#define GPIO_12 12u
#define GPIO_13 13u
#define GPIO_14 14u
#define GPIO_15 15u
#define GPIO_16 16u
#define GPIO_17 17u
#define GPIO_18 18u
#define GPIO_19 19u
#define GPIO_20 20u
#define GPIO_21 21u
#define GPIO_22 22u
#define GPIO_23 23u
#define GPIO_24 24u
#define GPIO_25 25u
#define GPIO_26 26u
#define GPIO_27 27u
#define GPIO_28 28u
#define GPIO_29 29u
#define GPIO_30 30u
#define GPIO_31 31u
#define GPIO_32 32u
#define GPIO_33 33u
#define GPIO_34 34u
#define GPIO_35 35u
#define GPIO_36 36u
#define GPIO_37 37u

#define NUM_OF_GPIOS 38u
typedef struct {
    volatile uint32_t *datal_reg_pointer;
    volatile uint32_t *datah_reg_pointer;
} GPIO;

void gpio_init(GPIO *const gpio);
void set_gpio(uint8_t pin);
void clear_gpio(uint8_t pin);
void set_or_clear_gpio(uint8_t pin, bool set);

#endif /* GPIO_H */
