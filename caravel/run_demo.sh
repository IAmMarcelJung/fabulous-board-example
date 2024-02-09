#!/usr/bin/env bash
set -ex

rshell cp ./demo/caravel_spi_vga_bram.mpy ${FLASH}
rshell cp ./demo/counter.bin ${FLASH}/counter.bin
sync
mpremote connect ${DEV} exec "import caravel_spi_vga_bram; caravel_spi_vga_bram.run()"
