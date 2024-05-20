# FABulous board example

## Summary

This repository documents how to upload a bitstream to a
[FABulous](https://github.com/FPGA-Research-Manchester/FABulous) eFPGA[^1]
fabricated in the [MPW-2](https://platform.efabless.com/shuttles/MPW-2) run of
the Open MPW Shuttle Program.
mounted on a [caravel
HAT](https://github.com/efabless/caravel_board/tree/main/hardware/nucleo/caravel_nucleo)[^2].
This HAT can either operate in standalone mode or be
mounted onto a [Nucleo
board](https://www.st.com/en/evaluation-tools/nucleo-f746zg.html#overview)[^3].

The process for using the Nucleo board is using bash scripts and Micropython and
is based on this
[forked base repository](https://github.com/gatecat/fabulous-mpw2-bringup)
(commit `34bcb9d`).

Also the test functionality from the [caravel board
repo](https://github.com/efabless/caravel_board/tree/main) (commit
`0eb8c4c`) is used, but with a bit of cleanup in the directory structure and
adjustments to the Makefiles and the flash script. It is mandatory to check a
chip for the failure pattern caused by the hold time violations in the GPIO
configuration module prior to uploading a bitstream. There are currently seven
pretested chips available at the University of Heidelberg. Each pretested chip
is labeled with its part number, starting at 0. If you test another chip in the
future, please also label it.

## Uploading a bitstream

There are two options for uploading a bitstream. Either the Nucleo board
used for the GPIO configuration testing or the Caravel board in standalone mode
can be used. The process for using the Nucleo board for a checked chip is
described in [caravel](./caravel) and in [gpio_test](./gpio_test) for the
standalone mode.

## General Information

In `fabric/verilog/eFPGA_v3_top_sky130.v` the mappings of the HAT
IO-Pins to the internal pins can be found. However, the pins are shifted by an
offset of 7
because the first 7 pins are used by Caravel.
Therefore `io_in[0]` corresponds to `IO_7` in the micropython code and
so on. A few IOs are also already assigned inside the fabric as follows:

| HAT         | FPGA     | Micropython | Function       |
|-------------|----------|-------------|----------------|
|  IO[7]      | io_in[0] | IO_7        | external clock |
|  IO[8]      | io_in[1] | IO_8        | clock select 0 |
|  IO[9]      | io_in[2] | IO_9        | clock select 1 |
|  IO[10]     | io_in[3] | IO_10       | serial clock   |
|  IO[11]     | io_in[4] | IO_11       | serial data    |
|  IO[12]     | io_in[5] | IO_12       | UART RX        |
|  IO[13]     | io_out[6] | IO_13       | RX LED        |

Pins `IO14`/`io_in[7]` and higher can be used in the user design.

### Clock selection

By setting `IO_8` and `IO_9`, the clock used for the eFPGA can be selected.
The selection is defined in `fabric/verilog/eFPGA_v3_top_sky130.v` as follows:

| IO_8 | IO_9 | clock source        |
|------|------|---------------------|
|  0   |  X   | external (IO_7)     |
|  1   |  0   | wishbone (10 MHz)   |
|  1   |  1   | user                |

## Resources

- [GPIO diagnostic](https://github.com/efabless/caravel_board/tree/main/firmware/mpw2-5/nucleo)
- [FABulous](https://github.com/FPGA-Research-Manchester/FABulous)
- [Caravel HAT](https://github.com/efabless/caravel_board/tree/main/hardware/nucleo/caravel_nucleo)

[^1]: this will be referred to as "eFPGA".
[^2]: this will be referred to as "HAT".
[^3]: this will be referred to as "the board", "board", "Nucleo" or "Nucleo
  board".
