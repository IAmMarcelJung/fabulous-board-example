#include <upload_bitstream.h>

#define PIN_SCLK IO_10_DATA_BIT_POS
#define PIN_SDATA IO_11_DATA_BIT_POS

#define CTRL_WORD_DISABLE_BITBANG 0x0000FAB0
#define CTRL_WORD_ENABLE_BITBANG 0x0000FAB1

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
        for (uint32_t bit_pos = 0u; bit_pos < sizeof(uint8_t); bit_pos++) {
            bool set;
            set = (bool)(bitstream_data[byte_pos] >> (7u - bit_pos) & 0x1u);
            set_or_clear_pin(PIN_SDATA, LOW_CHAIN, set);
            set_pin(PIN_SCLK, LOW_CHAIN);
            set = (bool)(CTRL_WORD_ENABLE_BITBANG >>
                    (31u - (8u * (byte_pos % 4u) + bit_pos)) &
                    0x1u);
            set_or_clear_pin(PIN_SDATA, LOW_CHAIN, set);
            clear_pin(PIN_SCLK, LOW_CHAIN);
        }
    }
}
