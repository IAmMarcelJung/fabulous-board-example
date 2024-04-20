#include <io_def_mock.h>

DEFINE_FAKE_VOID_FUNC(set_pin, uint8_t, te_chain);
DEFINE_FAKE_VOID_FUNC(clear_pin, uint8_t, te_chain);
DEFINE_FAKE_VOID_FUNC(set_or_clear_pin, uint8_t, te_chain, bool);

#include <stdio.h>

void write_bit_to_file(uint8_t val);

void my_fake(uint8_t pin, te_chain chain, bool set)
{
    write_bit_to_file((uint8_t)set);
}


void write_bit_to_file(uint8_t val)
{
    FILE *fd;
    fd = fopen("transmitted_data.txt", "a");

    if (fd == NULL)
    {
        printf("Failed to open the file.\n");
    }

    fprintf(fd, "%d", val);

    fclose(fd);
}
