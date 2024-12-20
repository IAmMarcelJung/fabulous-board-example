# FABulous board example

## Summary

This repository serves multiple purposes: It includes python files to upload a bitstream to a
[FABulous](https://github.com/FPGA-Research-Manchester/FABulous) eFPGA[^1]
fabricated in the [MPW-2](https://platform.efabless.com/shuttles/MPW-2) run of
the Open MPW Shuttle Program
mounted on a [caravel
HAT](https://github.com/efabless/caravel_board/tree/main/hardware/nucleo/caravel_nucleo)[^2].
This HAT can either operate in standalone mode or be
mounted onto a [Nucleo
board](https://www.st.com/en/evaluation-tools/nucleo-f746zg.html#overview)[^3].
Another purpose is the flashing of the caravel SoC firmware so that a bitstream
can be uploaded to the eFPGA and the outputs are available.

The process for using the Nucleo board is using bash scripts and MicroPython
It is based on this
[forked base repository](https://github.com/gatecat/fabulous-mpw2-bringup)
(commit `34bcb9d`).

Also, the test functionality from the [caravel board
repo](https://github.com/efabless/caravel_board/tree/main) (commit `0eb8c4c`) is
used, but with a bit of cleanup in the directory structure and adjustments to
the Makefiles and the flash script. It is mandatory to check a chip for the
failure pattern caused by the hold time violations in the GPIO configuration
module prior to uploading a bitstream. There are currently seven pretested chips
available at the University of Heidelberg. Eight more chips are also labeled, but
since they were not factory soldered they still have some issues. Each pretested
chip is labeled with its part number, starting at 0. If you test another chip in
the future, please also label it.

## Project structure

- `bitstream_upload_python`: Files for using the Nucleo board to upload a bitstream.
- `mpw2_fabric`: Files of the hardware fabric on the MPW-2 chip.
- `gpio_test`: Directories for checking the GPIO configuration failure pattern
  and for uploading the bitstream in standalone mode. Also contains a directory
  for tests of the modules used in the firmware.
- `output_files`: Output files of many actions inside the repository. Also, the
  bitstream (or a link to it) should be placed here.
- `sim`: Files for simulation of the whole fabric including uploading the
  bitstream of the user design.
- `user_design`: Example user designs. Mostly taken from the base repo and also
untested.

## Uploading a bitstream

There are two options for uploading a bitstream. Either the Nucleo board
used for the GPIO configuration testing or the Caravel board in standalone mode
can be used. The process for using the Nucleo board for a checked chip is
described in [bitstream_upload_python](./bitstream_upload_python) and in
[gpio_test](./gpio_test) for the standalone mode.

## IO Mapping

In `mpw2_fabric/verilog/eFPGA_v3_top_sky130.v` the mappings of the HAT
IO-Pins to the internal pins can be found. However, the pins are shifted by an
offset of 7
because the first 7 pins are used by Caravel.
Therefore, `io_in[0]` corresponds to `IO_7` in the MicroPython code and
so on. A few IOs are also already assigned inside the fabric as follows:

| HAT         | eFPGA     | MicroPython | Function      |
|-------------|-----------|------------|----------------|
|  IO[7]      | io_in[0]  |    IO_7    | external clock |
|  IO[8]      | io_in[1]  |    IO_8    | clock select 0 |
|  IO[9]      | io_in[2]  |    IO_9    | clock select 1 |
|  IO[10]     | io_in[3]  |    IO_10   | serial clock   |
|  IO[11]     | io_in[4]  |    IO_11   | serial data    |
|  IO[12]     | io_in[5]  |    IO_12   | UART RX        |
|  IO[13]     | io_out[6] |    IO_13   | RX LED         |


### Clock selection

By setting `IO_8` and `IO_9`, the clock used for the eFPGA can be selected.
The selection is defined in `mpw2_fabric/verilog/eFPGA_v3_top_sky130.v` as follows:

| IO_8 | IO_9 | clock source        |
|------|------|---------------------|
|  0   |  X   | external (IO_7)     |
|  1   |  0   | wishbone (10 MHz)   |
|  1   |  1   | user                |

> Note
> The clock cannot be selected for MPW-5 eFPGAs, since the `io_oeb` bits of the
> fabric pins a not set correctly.

### User design mapping
Pins `IO[14]`/`io_in/out[7]` and higher can be used in the user design, so the
pins are shifted by another seven pins compared to the eFPGA pins. The
table below shows the whole mapping. Note that if e.g. the bitbang configuration
from inside Caravel is used, these pins also have to be assigned to one of the
HAT pins `IO[14]` to `IO[37]`.

| HAT | User Design |
|------|------|
|  IO[14]  |  io_in/out[0]   |
|  IO[15]  |  io_in/out[1]   |
|  IO[16]  |  io_in/out[2]   |
|  IO[17]  |  io_in/out[3]   |
|  IO[18]  |  io_in/out[4]   |
|  IO[19]  |  io_in/out[5]   |
|  IO[20]  |  io_in/out[6]   |
|  IO[21]  |  io_in/out[7]   |
|  IO[22]  |  io_in/out[8]   |
|  IO[23]  |  io_in/out[9]   |
|  IO[24]  |  io_in/out[10]   |
|  IO[25]  |  io_in/out[11]   |
|  IO[26]  |  io_in/out[12]   |
|  IO[27]  |  io_in/out[13]   |
|  IO[28]  |  io_in/out[14]   |
|  IO[29]  |  io_in/out[15]   |
|  IO[30]  |  io_in/out[16]   |
|  IO[31]  |  io_in/out[17]   |
|  IO[32]  |  io_in/out[18]   |
|  IO[33]  |  io_in/out[19]   |
|  IO[34]  |  io_in/out[20]   |
|  IO[35]  |  io_in/out[21]   |
|  IO[36]  |  io_in/out[22]   |
|  IO[37]  |  io_in/out[23]   |

## Resources

- [GPIO diagnostic](https://github.com/efabless/caravel_board/tree/main/firmware/mpw2-5/nucleo)
- [FABulous](https://github.com/FPGA-Research-Manchester/FABulous)
- [Caravel HAT](https://github.com/efabless/caravel_board/tree/main/hardware/nucleo/caravel_nucleo)

[^1]: this will be referred to as "eFPGA".
[^2]: this will be referred to as "HAT".
[^3]: this will be referred to as "the board", "board", "Nucleo" or "Nucleo
  board".
