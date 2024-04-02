#!/usr/bin/env bash
set -ex

DEV=$(mpremote connect list | grep STLink | cut -f 1 -d ' ')

mpy-cross caravel_spi.py
mpy-cross modules/board.py
mpy-cross modules/myspi.py

rshell --port ${DEV} mkdir ${FLASH}/modules/

rshell --port ${DEV} cp caravel_spi.mpy ${FLASH}
rshell --port ${DEV} cp modules/board.mpy ${FLASH}/modules/
rshell --port ${DEV} cp modules/myspi.mpy ${FLASH}/modules/

rshell --port ${DEV} cp ../sim/test_design/${DESIGN}/${DESIGN}.bin ${FLASH}/counter.bin
sync
mpremote connect ${DEV} exec "import caravel_spi; caravel_spi.run()"
