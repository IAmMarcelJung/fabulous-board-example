#!/usr/bin/env bash
set -ex

mpy-cross caravel_spi.py
rshell cp caravel_spi.mpy ${FLASH}
rshell cp ../sim/test_design/${DESIGN}.bin ${FLASH}/counter.bin
sync
mpremote connect ${DEV} exec "import caravel_spi; caravel_spi.run()"
