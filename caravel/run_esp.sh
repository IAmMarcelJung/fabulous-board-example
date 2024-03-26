#!/usr/bin/env bash
set -ex

mpy-cross caravel_esp.py
mpy-cross modules/board.py
mpy-cross modules/myspi.py


rshell -p ${ESP_DEV} mkdir ${ESP_FLASH}/modules/

rshell -p ${ESP_DEV} cp caravel_esp.mpy ${ESP_FLASH}
rshell  -p ${ESP_DEV} cp modules/board.mpy ${ESP_FLASH}/modules/
rshell -p ${ESP_DEV} cp modules/myspi.mpy ${ESP_FLASH}/modules/

rshell -p ${ESP_DEV} cp ../sim/test_design/${DESIGN}/${DESIGN}.bin ${ESP_FLASH}/counter.bin
sync
mpremote connect ${ESP_DEV} exec "import caravel_esp; caravel_esp.run()"
