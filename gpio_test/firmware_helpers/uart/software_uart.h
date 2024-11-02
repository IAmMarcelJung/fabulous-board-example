#ifndef SOFTWARE_UART_H
#define SOFTWARE_UART_H

#include <stdint.h>

// UART configuration
#define CPU_FREQ 10000000 // 10 MHz
#define BAUD_RATE_MPW_5 46080
#define BAUD_RATE_MPW_2 57600

// Timer configuration bits
#define TIMER_ENABLE 0x01
#define TIMER_ONESHOT 0x02
#define TIMER_UPCOUNT 0x04

typedef enum { EVEN, ODD } te_parity;

// UART structure to hold configuration
typedef struct {
    uint32_t baud_rate; // Baud rate (default 46080)
    te_parity parity;
} uart_config_t;

void software_uart_init(uart_config_t const *const config);
void software_uart_tx_byte(uint8_t const byte);

#endif /* SOFTWARE_UART_H */
