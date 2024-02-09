#!/usr/bin/env bash
set -ex

rshell cp ./demo/counter.bin ${FLASH}
sync
mpremote connect ${DEV} exec "import caravel_spi_vga_bram; caravel_spi_vga_bram.run()"