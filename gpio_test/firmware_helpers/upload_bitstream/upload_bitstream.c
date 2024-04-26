#include <global_defs.h>
#include <defs.h>
#include <upload_bitstream.h>
#include <register_actions.h>

#define PIN_SCLK GPIO_10
#define PIN_SDATA GPIO_11

#define CTRL_WORD_DISABLE_BITBANG 0x0000FAB0u
#define CTRL_WORD_ENABLE_BITBANG 0x0000FAB1u

#define EXTRACT_BYTE_FROM_WORD(word, byte_index) (((word) >> (BITS_IN_BYTE * byte_index)) & 0xFFu)
#define GET_BIT_AS_BOOL_FROM_BYTE(byte, index) ((bool)(((byte) >> (index)) & 0x01u))
#define MODULO_4(data) data & 0x03u // Just using the last two bits is effectively modulo 4

/**
 * @brief Use bitbanging to upload the bitstream to the FPGA.
 * @param bitstream_data The bitstream data to be transmitted to the FPGA.
 * @param bitream_size The bitstream size in bytes.
 * @param ctrl_word The control word used to control the bitbang module.
 */
void upload_bitstream(uint8_t const *const bitstream_data,
        uint32_t bitream_size)
{
    for (uint32_t byte_pos = 0u; byte_pos < bitream_size; byte_pos++) {
        reg_gpio_out = ~reg_gpio_out & 1u;
        uint8_t current_byte = bitstream_data[byte_pos];
        uint8_t control_word_byte_pos = ~MODULO_4(byte_pos); // Invert because we want to start from the most significant byte.
        uint8_t current_control_word_byte = EXTRACT_BYTE_FROM_WORD(CTRL_WORD_ENABLE_BITBANG, control_word_byte_pos);
        for (int32_t bit_pos = (int32_t)MSB_IN_BYTE; bit_pos >= 0; bit_pos--) {
            bool set;
            set = (bool)(bitstream_data[byte_pos] >> (MSB_IN_BYTE - bit_pos) & 1u);
            set_or_clear_pin(PIN_SDATA, set);
            set_pin(PIN_SCLK);
            set = (bool)(CTRL_WORD_ENABLE_BITBANG >>
                    (MSB_IN_WORD - (BYTES_IN_WORD * (byte_pos % BYTES_IN_WORD) + bit_pos)) &
                    1u);
            set_or_clear_pin(PIN_SDATA, set);
            clear_pin(PIN_SCLK);
        }
    }
}
