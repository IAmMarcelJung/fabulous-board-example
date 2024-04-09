#!/usr/bin/env bash

DEV=$(mpremote connect list | grep STLink | cut -f 1 -d ' ')
RSHELL_PORT="rshell --port ${DEV}"
COPY_CMD="${RSHELL_PORT} cp"
MKDIR_CMD="${RSHELL_PORT} mkdir"

set -ex

mpy-cross fabulous_demo.py
mpy-cross ./modules/board.py
mpy-cross ./modules/myspi.py

${COPY_CMD} fabulous_demo.mpy ${FLASH}

${MKDIR_CMD} ${FLASH}/modules

${COPY_CMD} ./modules/myspi.mpy ${FLASH}/modules/
${COPY_CMD} ./modules/board.mpy ${FLASH}/modules/
${COPY_CMD} ./../output_files/bitstream.bin ${FLASH}
${COPY_CMD} ./street.bin ${FLASH}

sync
mpremote connect ${DEV} exec "import fabulous_demo; fabulous_demo.run()"
