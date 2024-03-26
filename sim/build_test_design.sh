#!/usr/bin/env bash

SYNTH_TCL=${HOME}/${FABPATH}/fabric_cad/synth/synth_fabulous.tcl
BIT_GEN=${HOME}/${FABPATH}/fabric_cad/bit_gen.py
DESIGN=$1

set -ex
yosys -p "synth_fabulous -complex-dff -carry ha -top top_wrapper -json test_design/${DESIGN}/${DESIGN}.json" test_design/${DESIGN}/${DESIGN}.v test_design/top_wrapper.v

FAB_ROOT=../fabric nextpnr-generic --timing-allow-fail --verbose --log nextpnr_log.txt --uarch fabulous --json test_design/${DESIGN}/${DESIGN}.json -o fasm=test_design/${DESIGN}/${DESIGN}.fasm

python3 ${BIT_GEN} -genBitstream test_design/${DESIGN}/${DESIGN}.fasm ../fabric/npnroutput/meta_data.txt test_design/${DESIGN}/${DESIGN}.bin
