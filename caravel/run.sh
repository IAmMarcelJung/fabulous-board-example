#!/usr/bin/env bash
set -ex

module=$1

if [ -z "$module" ]; then
    echo "Please specify the module containing run()"
else

    mpy-cross $module.py
    mpy-cross modules/board.py
    mpy-cross modules/myspi.py
    cp ../output_files/bitstream.bin .

    sync
    mpremote mount . exec "import $module; $module.run()"
    rm bitstream.bin
fi
