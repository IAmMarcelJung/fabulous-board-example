# FABulous board example

## Summary

This repository documents the uploading of a bitstream to a
[caravel HAT](https://github.com/efabless/caravel_board/tree/main/hardware/nucleo/caravel_nucleo)
mounted onto a [Nucleo
board](https://www.st.com/en/evaluation-tools/nucleo-f746zg.html#overview) as
far as it is known. All files for doing so are taken from the [forked base
repository](https://github.com/gatecat/fabulous-mpw2-bringup).
There also might be other ways to to
upload the bitstream, but only this one is currently known. If you find other
(and simpler) ways, feel free to share them.

## Prerequisites

The upload process is based on a script calling micropython modules, so you
need to install [mpremote](https://pypi.org/project/mpremote) and
[rshell](https://pypi.org/project/rshell/). To be able to compile your own
micropython file, also install  [mpy-cross](https://pypi.org/project/mpy-cross/),
but this is not needed for the demo.
If you do not have
a bitstream yet, you first have to generate it using FABulous.

The files could also be manually copied with the file explorer or by manually
mounting the caravel board. If you prefer the latter method, just mount the board
and remove any occurrences of ```rshell``` in the scripts.

## Hardware

The board has to be connected over the ST-LINK USB Micro-B connector  ```CN1```
and the OTG connector ```CN13``` to the Nucleo board. If the GPIOs have not been
checked for timing failures for the currently used part, you have to follow
[this guide](https://github.com/efabless/caravel_board/tree/main/firmware/mpw2-5/nucleo)
first.

### PmodVGA wiring

In case the PmodVGA ever gets disconnected from the board, here is the wiring
for the demo:

| Caravel HAT | PmodVGA |
|-------------|---------|
|  IO[15]     |  HS     |
|  IO[16]     |  VS     |
|  IO[17]     |  R3     |
|  IO[18]     |  G3     |
|  IO[19]     |  B3     |
|  IO[22]     |  R2     |
|  IO[23]     |  G2     |
|  IO[24]     |  B2     |
|  GND        |  GND    |
|  3V3        |  3V3    |

## Uploading a bitstream

First you
need to set the environment variables ```FLASH``` and ```DEV```. ```FLASH``` has
to be set to ```/pyboard/flash/```, which is the run directory on the board.
```DEV``` is the port on which the board is
connected (probably ```/dev/ttyACM1```). A way to easily manage the environment
variables is [direnv](https://github.com/direnv/direnv).

To run the demo, just execute ```run_demo_initial.sh```, if the board has never been
set up, and ```run.sh``` if the board has already been set up before. It might
take a few seconds before the demo is shown correctly even after the script has
finished, though but this is not always the case.

If you want to upload your own bitstream, place the bitstream in the ```caravel```
directory and set the ```DESIGN``` environment variable to your design name (e.g.
```sequential_16bit_en```). Also adjust ```caravel.spi``` to your needs.
Then run ```run.sh```.

## Additional Information

In ```fabric/verilog/eFPGA_v3_top_sky130.v``` the mappings of the caraval HAT
IO-Pins to the internal pins can be found. However, the pins are shifted by 7
because the first 7 pins are used internally ```TODO: explain more detailed and
add reference```.
Therefore ```io_in[0]``` corresponds to ```IO_7``` in the micropython code and
so on. A few IOs are already assigned as follows:

| Caravel HAT | eFPGA     | Micropython | Function       |
|-------------|----------|-------------|----------------|
|  IO[7]      | io_in[0] | IO_7        | external clock |
|  IO[8]      | io_in[1] | IO_8        | clock select 0 |
|  IO[9]      | io_in[2] | IO_9        | clock select 1 |
|  IO[10]     | io_in[3] | IO_10       | serial clock   |
|  IO[11]     | io_in[4] | IO_11       | serial data    |
|  IO[12]     | io_in[5] | IO_12       | UART RX        |
|  IO[13]     | io_out[6] | IO_13       | RX LED        |

Pins ```io_in[7]``` and higher can be used in the user design.

### Clock selection

By setting ```IO_8``` and ```IO_9``` the clock used for the fpga can be selected.
It is also defined in ```fabric/verilog/eFPGA_v3_top_sky130.v``` as follows:
| IO_8 | IO_9 | clock source |
|------|------|--------------|
|  0   |  X   | external     |
|  1   |  0   | wishbone     |
|  1   |  1   | user         |

## Resources

- [GPIO diagnostic](https://github.com/efabless/caravel_board/tree/main/firmware/mpw2-5/nucleo)
- [FABulous](https://github.com/FPGA-Research-Manchester/FABulous)
- [Caravel HAT](https://github.com/efabless/caravel_board/tree/main/hardware/nucleo/caravel_nucleo)
