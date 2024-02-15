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

## Hardware

The board has to be connected over the ST-LINK USB Micro-B connector  ```CN1```
to the Nucleo board. If you want to check the GPIOs for timing failures, you
also have to connect to ```CN13``` and follow
[this guide](https://github.com/efabless/caravel_board/tree/main/firmware/mpw2-5/nucleo)

### PmodVGA wiring

In case the PmodVGA ever gets disconnected from the board, here is the wiring for
the demo:

- IO[15] => HS
- IO[16] => VS
- IO[17] => R3
- IO[18] => G3
- IO[19] => B3
- IO[22] => R2
- IO[23] => G2
- IO[24] => B2
- GND => GND
- 3V3 => 3V3

## Uploading a bitstream

First you
need to set the enironment variables ```FLASH``` and ```DEV```. ```FLASH``` has
to be set to ```/pyboard/flash/```, which is the run directory on the board.
```DEV``` is the port on which the board is
connected (probably ```/dev/ttyACM0```).

To run the demo, just execute ```run_demo_initial.sh```, if the board has never been
set up, and ```run.sh``` if the board has already been set up before. It might
take a few seconds before the demo is shown correctly even after the script has
finished, though but this is not always the case.

If you want to upload your own bitstream, place the bitstream in the ```caravel```
directory and set the ```DESIGN``` environment variable to your design name (e.g.
```sequential_16bit_en```). Also adjust ```caravel.spi``` to your needs.
Then run ```run.sh```.

## Resources

- [GPIO diagnostic](https://github.com/efabless/caravel_board/tree/main/firmware/mpw2-5/nucleo)
- [FABulous](https://github.com/FPGA-Research-Manchester/FABulous)
- [Caravel HAT](https://github.com/efabless/caravel_board/tree/main/hardware/nucleo/caravel_nucleo)
