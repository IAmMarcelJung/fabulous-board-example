#ifndef REGISTER_ACTIONS_H
#define REGISTER_ACTIONS_H

#include <stdbool.h>
#include <stdint.h>

// Definitons register bits
#define REGISTER_0_DATA_BIT_POS 0
#define REGISTER_1_DATA_BIT_POS 1
#define REGISTER_2_DATA_BIT_POS 2
#define REGISTER_3_DATA_BIT_POS 3
#define REGISTER_4_DATA_BIT_POS 4
#define REGISTER_5_DATA_BIT_POS 5
#define REGISTER_6_DATA_BIT_POS 6
#define REGISTER_7_DATA_BIT_POS 7
#define REGISTER_8_DATA_BIT_POS 8
#define REGISTER_9_DATA_BIT_POS 9
#define REGISTER_10_DATA_BIT_POS 10
#define REGISTER_11_DATA_BIT_POS 11
#define REGISTER_12_DATA_BIT_POS 12
#define REGISTER_13_DATA_BIT_POS 13
#define REGISTER_14_DATA_BIT_POS 14
#define REGISTER_15_DATA_BIT_POS 15
#define REGISTER_16_DATA_BIT_POS 16
#define REGISTER_17_DATA_BIT_POS 17
#define REGISTER_18_DATA_BIT_POS 18
#define REGISTER_19_DATA_BIT_POS 19
#define REGISTER_20_DATA_BIT_POS 20
#define REGISTER_21_DATA_BIT_POS 21
#define REGISTER_22_DATA_BIT_POS 22
#define REGISTER_23_DATA_BIT_POS 23
#define REGISTER_24_DATA_BIT_POS 24
#define REGISTER_25_DATA_BIT_POS 25
#define REGISTER_26_DATA_BIT_POS 26
#define REGISTER_27_DATA_BIT_POS 27
#define REGISTER_28_DATA_BIT_POS 28
#define REGISTER_29_DATA_BIT_POS 29
#define REGISTER_30_DATA_BIT_POS 30
#define REGISTER_31_DATA_BIT_POS 31

#define REGISTER_DATA_BIT_MSK(bit) (0x1 << (bit))
#define REGISTER_DATA_BIT(bit) REGISTER_DATA_BIT_MSK(bit)

extern void set_bit(uint8_t bit, volatile uint32_t *const reg);
extern void clear_bit(uint8_t bit, volatile uint32_t *const reg);
extern void set_or_clear_bit(uint8_t bit, volatile uint32_t *const reg,
                             bool set);

#endif /* REGISTER_ACTIONS_H */
