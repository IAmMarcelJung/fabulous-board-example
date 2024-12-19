#include "../gpio_config/gpio_config_io.h"
#include <bitstream.h>
#include <helpers.h>
#include <software_uart.h>

void toggle_gpio_10000_times(void) {
    __asm__ volatile(
        "li t0, 0xf0002814\n\t" // Load the GPIO address into t0
        "li t2, 10000\n\t"      // Load the loop counter (10,000) into t2
        "1:\n\t"                // Label for the loop start
        "lw t1, 0(t0)\n\t"      // Load the current GPIO value into t1
        "not t1, t1\n\t"        // Toggle the value (bitwise NOT)
        "sw t1, 0(t0)\n\t"      // Write the toggled value back to GPIO
        "addi t2, t2, -1\n\t"   // Decrement the counter t2
        //
        "li t4, 10\n\t"       // Load bit_time into t4 for delay loop
        "2:\n\t"              // Delay loop label
        "addi t4, t4, -1\n\t" // Decrement delay counter
        "bnez t4, 2b\n\t"     // If delay counter not zero, loop
        //
        "bnez t2, 1b\n\t" // If counter is not zero, loop back to label 1
        :
        :
        : "t0", "t1", "t2" // Specify that t0, t1, and t2 are clobbered
    );
}

int main() {

    __asm__ volatile(
        "csrci mstatus, 0x8"); // Clear MIE bit to disable global interrupts
    uint32_t mie;
    mie &= 0x0;
    __asm__ __volatile__("csrw mie, %0" : : "r"(mie));
    uart_config_t uart_config = {.baud_rate = BAUD_RATE_MPW_5, .parity = ODD};
    software_uart_init(&uart_config);
    uint8_t bitstream_frames[20000][11];

    // uint32_t bitstream_size = sizeof(bitstream) / sizeof(uint8_t);
    uint32_t bitstream_size = 10u;

    reg_gpio_out = 1u;
    delay(20000000);
    toggle_gpio_10000_times();
    for (uint32_t i = 0u; i < 10000u; i++) {
        *(volatile uint32_t *)0xf0002814L = 0u;
        delay(10);
        *(volatile uint32_t *)0xf0002814L = 1u;
    }
    delay(20000000);

    for (uint32_t byte_pos = 0u; byte_pos < bitstream_size; byte_pos++) {
        uint8_t byte = bitstream[byte_pos];
        software_uart_tx_byte(byte);
        // TODO: test how long to wait between two frames
        delay(100);
    }
    uint16_t frame = (1 << 9) | (1 << 8) | (0 << 7) | (1 << 6) | (0 << 5) |
                     (1 << 4) | (0 << 3) | (1 << 2) | (0 << 1) | 0;
    register uint32_t bit_time = 117;
    register uint16_t tmp = frame;
    delay(bit_time);

    *(volatile uint32_t *)0xf0002814L = 1u;
    delay(bit_time);

    // for (uint8_t bit_pos = 0; bit_pos < UART_FRAME_SIZE; bit_pos++) {
    //     reg_gpio_out = (tmp >> bit_pos) & 0x1u; // Extract the bit at
    //     `bit_pos`
    //     // delay(bit_time);
    // }
    // Manually unroll each bit position
    *(volatile uint32_t *)0xf0002814L = (tmp >> 0);
    delay(bit_time);

    *(volatile uint32_t *)0xf0002814L = (tmp >> 1);
    delay(bit_time);

    *(volatile uint32_t *)0xf0002814L = (tmp >> 2);
    delay(bit_time);

    *(volatile uint32_t *)0xf0002814L = (tmp >> 3);
    delay(bit_time);

    *(volatile uint32_t *)0xf0002814L = (tmp >> 4);
    delay(bit_time);

    *(volatile uint32_t *)0xf0002814L = (tmp >> 5);
    delay(bit_time);

    *(volatile uint32_t *)0xf0002814L = (tmp >> 6);
    delay(bit_time);

    *(volatile uint32_t *)0xf0002814L = (tmp >> 7);
    delay(bit_time);

    *(volatile uint32_t *)0xf0002814L = (tmp >> 8);
    delay(bit_time);

    *(volatile uint32_t *)0xf0002814L = (tmp >> 9);
    delay(bit_time);

    *(volatile uint32_t *)0xf0002814L = 1u;
    delay(bit_time);

    delay(100);
    // blink(5u, 5000000u);

    gpio_config_io();
    // blink(5u, 2500000u);
    reg_gpio_out = 0u;

    while (1)
        ;

    return 0;
}
