#!/usr/bin/env bash
set -ex

# Strip .py from the command line argument so both the module and the file name
# can be specified
module="${1%.py}"

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
