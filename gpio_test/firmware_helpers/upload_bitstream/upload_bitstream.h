#ifndef UPLOAD_BITSTREAM_H
#define UPLOAD_BITSTREAM_H

#include <gpio.h>

void bitstream_init(GPIO *const gpio);
void upload_bitstream(uint8_t const *const bitstream_data, uint32_t bitstream);

#endif /* UPLOAD_BITSTREAM_H */
