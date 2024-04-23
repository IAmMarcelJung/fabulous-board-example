#include <gpio_mock.h>

DEFINE_FAKE_VOID_FUNC(set_gpio, uint8_t);
DEFINE_FAKE_VOID_FUNC(clear_gpio, uint8_t);
DEFINE_FAKE_VOID_FUNC(set_or_clear_gpio, uint8_t, bool);

#include <stdio.h>

/**
 * @brief Helper function to write a bit to a file
 * @param unused Unused value, just needed to have the correct signature.
 * @param set The flag to signalize if the bit should be set. Used here to
 * differ if 1 or 0 will be written to the file.
 */
void write_bit_to_file(uint8_t unused, bool set)
{
    FILE *fd;
    fd = fopen("transmitted_data.txt", "a");

    if (fd == NULL)
    {
        printf("Failed to open the file.\n");
    }

    fprintf(fd, "%d", (uint8_t)set & 1u);

    fclose(fd);
}
