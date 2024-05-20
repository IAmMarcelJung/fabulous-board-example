# GPIO test

This directory contains files to flash the Nucleo firmware to the Nucleo board,
check the GPIO configuration for the hold time violation type and flash the
firmware to set the GPIO configuration and upload the bitstream to the caravel SoC.

The base functionality is taken from the [caravel board repository](https://github.com/efabless/caravel_board/tree/main)
(commit `0eb8c4c`) and has been modified by changing the directory
structure, cleaning up some files and add some functionality to improve the
usability. Also modules for uploading the bitstream to the eFPGA have been
added.
The core functionality for checking the failure pattern was however
not changed.

The directories contain the following:

- `build_custom_firmware`: A variation of `build_firmware_template`.
- `build_firmware_template`: A template directory for creating the SoC firmware
to configure the GPIOs and upload the bitstream.
- `generated`: Some generated files needed for the RISC-V firmware. No changes
were made. It is unclear how these files were originally generated so they will
not be regenerated here.
- `gpio_config`: Scripts and files needed for the GPIO configuration.
- `hw`: Only contains common.h.
- `nucleo_firmware`: All files needed to flash the Nucleo board. Also contains
  the firmware to check the GPIO configuration for hold time violations.
- `riscv_firmware_src`: Files related to the RISC-V firmware for the caravel
SoC.
- `util`: Contains scripts to interact with the caravel SoC when it is
  used as a standalone device.
