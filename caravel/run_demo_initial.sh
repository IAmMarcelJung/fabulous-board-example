#!/usr/bin/env bash
set -ex

mpy-cross caravel_spi_vga_bram.py
mpy-cross ./modules/board.py
mpy-cross ./modules/myspi.py

rshell mkdir ${FLASH}/modules
rshell cp ./modules/myspi.mpy ${FLASH}/modules/
rshell cp ./modules/board.mpy ${FLASH}/modules/
cp caravel_spi_vga_bram.mpy ./demo/
rshell cp ./demo/* ${FLASH}
sync
mpremote connect ${DEV} exec "import caravel_spi_vga_bram; caravel_spi_vga_bram.run()"
