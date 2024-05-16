#!/usr/bin/env bash
set -ex
DESIGN=counter
OUTPUT=../output_files
BITSTREAM=${OUTPUT}/bitstream.bin
VERILOG=../fabric/verilog
MAX_BITBYTES=16384
USER_DESIGN=../user_design/

python3 makehex.py $BITSTREAM $MAX_BITBYTES ${OUTPUT}/bitstream.hex
iverilog -s fab_tb -o ${OUTPUT}/fab_tb.vvp $VERILOG/*.v ${USER_DESIGN}/${DESIGN}/${DESIGN}.v fabulous_tb.v models_pack.v ${IVFLAGS} -DCREATE_VCD -DCREATE_FST
vvp $OUTPUT/fab_tb.vvp -fst
