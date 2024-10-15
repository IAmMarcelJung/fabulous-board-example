#include "custom_uart.h"
#include <defs.h>
#include <gpio_config_io.h>

// Shadow register state
static uint32_t gpio_shadow_low = 0;  // Shadow for GPIO 0-31
static uint32_t gpio_shadow_high = 0; // Shadow for GPIO 32-37

static int gpio_update_registers(void) {
    // Write complete shadow registers to hardware
    reg_mprj_datal = gpio_shadow_low;
    reg_mprj_datah = gpio_shadow_high;
    return UART_SUCCESS;
}

static int gpio_write(uint8_t pin, uint8_t value) {
    if (pin > MAX_GPIO_PIN) {
        return UART_ERR_PIN;
    }

    if (pin < 32) {
        // Lower bank of GPIOs
        if (value) {
            gpio_shadow_low |= (1u << pin);
        } else {
            gpio_shadow_low &= ~(1u << pin);
        }
    } else {
        // Upper bank of GPIOs (pin 32-37)
        pin -= 32; // Adjust to 0-5 range for upper bank
        if (value) {
            gpio_shadow_high |= (1u << pin);
        } else {
            gpio_shadow_high &= ~(1u << pin);
        }
    }

    return gpio_update_registers();
}

static int start_timer(uint32_t cycles) {
    reg_timer0_config = 0;
    reg_timer0_data = cycles;
    reg_timer0_config = TIMER_ENABLE | TIMER_ONESHOT;
    return UART_SUCCESS;
}

static int wait_timer_complete(void) {
    uint32_t timeout = 0xFFFF;

    while (reg_timer0_value > 0) {
        if (--timeout == 0)
            return UART_ERR_TIMER;
        asm volatile("nop");
    }

    return UART_SUCCESS;
}

int uart_init(uart_config_t *config) {
    int status;

    // Validate pin number
    if (config->tx_pin > MAX_GPIO_PIN) {
        return UART_ERR_PIN;
    }

    // Initialize shadow registers with current GPIO states if needed
    // gpio_shadow_low = reg_mprj_datal;  // Uncomment if you need to preserve
    // existing states gpio_shadow_high = reg_mprj_datah;

    // Set TX pin high (idle state)
    status = gpio_write(config->tx_pin, 1);
    if (status != UART_SUCCESS)
        return status;

    // Initialize timer
    reg_timer0_config = 0;

    return UART_SUCCESS;
}

int uart_tx_byte(uart_config_t *config, uint8_t byte) {
    int status;

    // Start bit (low)
    status = gpio_write(config->tx_pin, 0);
    if (status != UART_SUCCESS)
        return status;

    delay(BIT_PERIOD);
    if (status != UART_SUCCESS)
        return status;

    // Data bits (LSB first)
    for (int i = 0; i < 8; i++) {
        status = gpio_write(config->tx_pin, (byte >> i) & 1);
        if (status != UART_SUCCESS)
            return status;

        delay(BIT_PERIOD);
        if (status != UART_SUCCESS)
            return status;
    }

    // Stop bit (high)
    status = gpio_write(config->tx_pin, 1);
    if (status != UART_SUCCESS)
        return status;

    delay(BIT_PERIOD);

    return UART_SUCCESS;
}

int uart_tx_string(uart_config_t *config, const char *str) {
    int status;
    while (*str) {
        status = uart_tx_byte(config, *str++);
        if (status != UART_SUCCESS)
            return status;
    }
    return UART_SUCCESS;
}

int uart_tx_hex(uart_config_t *config, uint32_t value) {
    static const char hex_chars[] = "0123456789ABCDEF";
    char buffer[9];

    for (int i = 7; i >= 0; i--) {
        buffer[i] = hex_chars[value & 0xF];
        value >>= 4;
    }
    buffer[8] = '\0';

    return uart_tx_string(config, buffer);
}
void test(uart_config_t *config) {
    for (int i = 0; i < MAX_GPIO_PIN; i++) {
        gpio_write(i, 0);
    }
    delay(250000);
    for (int i = 0; i < MAX_GPIO_PIN; i++) {
        gpio_write(i, 1);
    }
    delay(250000);
}
