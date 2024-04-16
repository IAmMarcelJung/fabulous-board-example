#ifndef IO_DEF_H
#define IO_DEF_H

#include <stdint.h>

// Definitons for the low chain
#define IO_0_DATA_BIT_POS 0 
#define IO_1_DATA_BIT_POS 1 
#define IO_2_DATA_BIT_POS 2 
#define IO_3_DATA_BIT_POS 3 
#define IO_4_DATA_BIT_POS 4 
#define IO_5_DATA_BIT_POS 5 
#define IO_6_DATA_BIT_POS 6 
#define IO_7_DATA_BIT_POS 7 
#define IO_8_DATA_BIT_POS 8 
#define IO_9_DATA_BIT_POS 9 
#define IO_10_DATA_BIT_POS 10 
#define IO_11_DATA_BIT_POS 11 
#define IO_12_DATA_BIT_POS 12 
#define IO_13_DATA_BIT_POS 13 
#define IO_14_DATA_BIT_POS 14 
#define IO_15_DATA_BIT_POS 15 
#define IO_16_DATA_BIT_POS 16 
#define IO_17_DATA_BIT_POS 17 
#define IO_18_DATA_BIT_POS 18 

// Definitons for the high chain
#define IO_19_DATA_BIT_POS 0 
#define IO_20_DATA_BIT_POS 1 
#define IO_21_DATA_BIT_POS 2 
#define IO_22_DATA_BIT_POS 3 
#define IO_23_DATA_BIT_POS 4 
#define IO_24_DATA_BIT_POS 5 
#define IO_25_DATA_BIT_POS 6 
#define IO_26_DATA_BIT_POS 7 
#define IO_27_DATA_BIT_POS 8 
#define IO_28_DATA_BIT_POS 9 
#define IO_29_DATA_BIT_POS 10 
#define IO_30_DATA_BIT_POS 11 
#define IO_31_DATA_BIT_POS 12 
#define IO_32_DATA_BIT_POS 13 
#define IO_33_DATA_BIT_POS 14 
#define IO_34_DATA_BIT_POS 15 
#define IO_35_DATA_BIT_POS 16 
#define IO_36_DATA_BIT_POS 17 
#define IO_37_DATA_BIT_POS 18 

#define IO_DATA_BIT_MSK(bit) (0x1 << (bit))
#define IO_DATA_BIT(bit) IO_DATA_BIT_MSK(bit)

typedef enum te_chain
{
    HIGH_CHAIN,
    LOW_CHAIN
} te_chain;

typedef uint8_t bool_t;

#define true 1
#define false 0

void set_pin(uint8_t pin, te_chain chain);
void clear_pin(uint8_t pin, te_chain chain);
void set_or_clear(uint8_t pin, te_chain, bool_t set);

#endif /* IO_DEF_H */
