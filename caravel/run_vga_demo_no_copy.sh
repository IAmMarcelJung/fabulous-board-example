#!/usr/bin/env bash
set -ex

mpy-cross fabulous_demo.py
mpy-cross modules/board.py
mpy-cross modules/myspi.py
cp ../output_files/bitstream.bin .

sync
mpremote mount . exec "import fabulous_demo; fabulous_demo.run()"
rm bitstream.bin
