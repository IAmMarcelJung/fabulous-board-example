#!/usr/bin/env bash
set -ex
DESIGN=counter
BITSTREAM=test_design/${DESIGN}/${DESIGN}.bin
VERILOG=../fabric/verilog
MAX_BITBYTES=16384
USER_DESIGN=../user_design/
OUTPUT=../output_files

iverilog -s fab_tb -o ${OUTPUT}/fab_tb.vvp $VERILOG/*.v ${USER_DESIGN}/${DESIGN}/${DESIGN}.v fabulous_tb.v models_pack.v ${IVFLAGS} -DCREATE_VCD
python3 makehex.py $BITSTREAM $MAX_BITBYTES ${OUTPUT}/bitstream.hex
vvp fab_tb.vvp -fst
