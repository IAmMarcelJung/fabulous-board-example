#!/usr/bin/env bash
set -ex
DESIGN=counter
BITSTREAM=test_design/${DESIGN}/${DESIGN}.bin
VERILOG=../fabric/verilog
MAX_BITBYTES=16384

iverilog -s fab_tb -o fab_tb.vvp $VERILOG/*.v test_design/${DESIGN}/${DESIGN}.v fabulous_tb.v models_pack.v ${IVFLAGS} -DCREATE_VCD
python3 makehex.py $BITSTREAM $MAX_BITBYTES bitstream.hex
vvp fab_tb.vvp -fst
