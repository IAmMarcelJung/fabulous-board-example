#include "upload_bistream.h"
#include "../riscv_firmware_src/defs.h"
#include "io_def.h"

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
void load_bitstream(uint8_t const * const bitstream_data, uint32_t bitream_size)
{
    for (uint32_t byte_pos = 0; byte_pos < bitream_size; byte_pos++)
    {
        for (uint32_t bit_pos = 0; bit_pos < sizeof(uint8_t); bit_pos++)
        {
            bool_t set;
            set = bool_t(bitstream_data[byte_pos] >> (7 - bit_pos) & 0x1);
            set_or_clear(PIN_SDATA, LOW_CHAIN, set);
            set_pin(PIN_SCLK, LOW_CHAIN);
            // TODO toggle sclk high
            set = (bool_t)(ctrl_word >> (31 - (8 * (byte_pos % 4) + bit_pos)) & 0x1);
            set_or_clear(PIN_SDATA, LOW_CHAIN, set);
            clear_pin(PIN_SCLK, LOW_CHAIN);
        }
    }
}
