# GPIO test

This directory contains files to check the GPIO configuration for
hold time violations and flash a custom firmware to to caravel Soc.

It is taken from the [caravel board repo](https://github.com/efabless/caravel_board/tree/main)
(commit ```0eb8c4c```)
with some minor modifications to the strucure and some files.

The directories contain the following:

- ```build_custom_firmware```: A variation of ```buid_firmware_template```
- ```riscv_firmware_src```: Files related to the RISC-V firmware for the caravel
SoC.
- ```build_firmware_template```: A template directory for creating a custom firmware.
The original name in the source was ```gpio_test```.
- ```generated```: Some generated files needed for the firmware. No changes were
made.
- ```gpio_config```: Scripts and files needed for the GPIO configuration.
- ```hw```: Only contains common.h.
- ```nucleo_firmware```: All files needed to flash the Nucleo board.
- ```util```: Conatains some scripts to interact with the caravel SoC.
