#ifndef _RAVENNA_IO_H_
#define _RAVENNA_IO_H_

#include <defs.h>

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wbuiltin-declaration-mismatch"
void putchar(uint32_t c);
#pragma GCC diagnostic pop
void print(const char *p);
void print_hex(uint32_t v, int digits);
void print_dec(uint32_t v);
void print_digit(uint32_t v);
char getchar_prompt(char *prompt);
uint32_t getchar();
void cmd_echo();

#endif
