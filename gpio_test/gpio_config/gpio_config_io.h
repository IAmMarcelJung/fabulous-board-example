#ifndef GPIO_CONFIG_IO_H
#define GPIO_CONFIG_IO_H

#define WAIT 50000

void delay(const int clock_cycles);

void bb_mode();

void load();

void clear_registers();

void gpio_config_io();

#endif /* GPIO_CONFIG_IO_H */
