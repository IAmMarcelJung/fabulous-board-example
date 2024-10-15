#ifndef CUSTOM_UART_H
#define CUSTOM_UART_H

#include <stdint.h>

// UART configuration
#define CPU_FREQ 10000000 // 10 MHz
#define BAUD_RATE 115200
#define BIT_PERIOD (CPU_FREQ / BAUD_RATE)

// Timer configuration bits
#define TIMER_ENABLE 0x01
#define TIMER_ONESHOT 0x02
#define TIMER_UPCOUNT 0x04

// Error codes
#define UART_SUCCESS 0
#define UART_ERR_TIMER 1
#define UART_ERR_GPIO 2
#define UART_ERR_PIN 3

// GPIO pin validation
#define MAX_GPIO_PIN 37 // Maximum GPIO pin number (32 low + 6 high)
//
// UART structure to hold configuration
typedef struct {
    uint8_t tx_pin;     // TX pin number (0-37)
    uint32_t baud_rate; // Baud rate (default 115200)
} uart_config_t;

int uart_init(uart_config_t *config);
int uart_tx_byte(uart_config_t *config, uint8_t byte);
int uart_tx_string(uart_config_t *config, const char *str);
int uart_tx_hex(uart_config_t *config, uint32_t value);
void test(uart_config_t *config);

#endif /* CUSTOM_UART */
