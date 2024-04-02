# FABulous board example

## Summary

This repository documents how to upload a bitstream to a
[FABulous](https://github.com/FPGA-Research-Manchester/FABulous) FPGA[^1]
mounted on a [caravel
HAT](https://github.com/efabless/caravel_board/tree/main/hardware/nucleo/caravel_nucleo)[^2]
mounted onto a [Nucleo
board](https://www.st.com/en/evaluation-tools/nucleo-f746zg.html#overview)[^3].
The process is using bash scripts and Micropython and is based on this [forked
base repository](https://github.com/gatecat/fabulous-mpw2-bringup) (commit ```34bcb9d```).
Also the test functionality from the [caravel board
repo](https://github.com/efabless/caravel_board/tree/main) (commit
```0eb8c4c```) is used, but with a bit of cleanup in the directory structure.
There are also other ways to to upload the files bitstream, but this one turned
out as the most reliable and fastest way.

[^1]: this will be referred to as "FPGA".
[^2]: this will be referred to as "HAT".
[^3]: this will be referred to as "the board", "board", "Nucleo" or "Nucleo
  board".

## TLDR to run the demo

Install [mpremote](https://pypi.org/project/mpremote)
and
[mpy-cross](https://pypi.org/project/mpy-cross/).

Connect a USB cable to ```CN1```.

> [!IMPORTANT]
> Be sure to wait a few seconds, until the HAT is fully powered on and
> the Power LED is on. Otherwise running the bitstream may silently
> fail.

Go to ```./caravel/```.

Run this command if the GPIO test process has already been executed and the
firmware has been flashed:

```console
mpremote mount . exec "import fabulous_demo; fabulous_demo.run()"
```

For an empty board without tested GPIOs and flashed firmware:

Follow [this guide](./gpio_test/nucleo_firmware/)
to check the pins for hold time violations.

## Prerequisites

The upload process is based on micropython modules, so you
need to install [mpremote](https://pypi.org/project/mpremote) for easy
communication with the Nucleo board.
To be able to compile your own
micropython file, also install  [mpy-cross](https://pypi.org/project/mpy-cross/),
but this is not needed if the board is already prepared for the demo.
If you do not have a bitstream yet, you first have to generate it
using [FABulous](https://github.com/FPGA-Research-Manchester/FABulous).

## Hardware

The host PC has to be connected over the ST-LINK USB Micro-B connector  ```CN1```
to the Nucleo board.

> [!IMPORTANT]
> Be sure to wait a few seconds, until the HAT is fully powered on and
> the Power LED is on. Otherwise running the bitstream may silently
> fail.

If the GPIOs have not been checked for timing failures for the currently used
part, you have to follow [this
guide](./gpio_test/nucleo_firmware/)
first.

### PmodVGA wiring

This is the wiring for the VGA demo.

| HAT | PmodVGA |
|-------------|---------|
|  IO[15]     |  HS     |
|  IO[16]     |  VS     |
|  IO[17]     |  R2     |
|  IO[18]     |  G2     |
|  IO[19]     |  B2     |
|  IO[22]     |  R3     |
|  IO[23]     |  G3     |
|  IO[24]     |  B3     |
|  GND        |  GND    |
|  3V3        |  3V3    |

## Uploading a bitstream

To run the demo, go to ```./caravel/``` and execute this command:

```console
mpremote mount . exec "import fabulous_demo; fabulous_demo.run()"
```

The demo is not directly displayed correctly, but this
should only last a few seconds, until the image data is loaded into the FPGA.

If you want to upload your own bitstream, place the bitstream in the
```sim/test_design/``` directory and set the ```DESIGN``` environment variable
to your design name (e.g. ```sequential_16bit_en```). Also adjust
```caravel_spi.py``` to your needs. Then run

```console
mpremote mount . exec "import caravel_spi; caravel_spi.run()"
```

Of course you can also come up with your own module.

## Additional Information

In ```fabric/verilog/eFPGA_v3_top_sky130.v``` the mappings of the HAT
IO-Pins to the internal pins can be found. However, the pins are shifted by an
offset of 7
because the first 7 pins are used by Caravel.
Therefore ```io_in[0]``` corresponds to ```IO_7``` in the micropython code and
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

Pins ```IO14```/```io_in[7]``` and higher can be used in the user design.

### Clock selection

By setting ```IO_8``` and ```IO_9```, the clock used for the FPGA can be selected.
The selection is defined in ```fabric/verilog/eFPGA_v3_top_sky130.v``` as follows:

| IO_8 | IO_9 | clock source        |
|------|------|---------------------|
|  0   |  X   | external (IO_7)     |
|  1   |  0   | wishbone (10 MHz)   |
|  1   |  1   | user                |

## Resources

- [GPIO diagnostic](https://github.com/efabless/caravel_board/tree/main/firmware/mpw2-5/nucleo)
- [FABulous](https://github.com/FPGA-Research-Manchester/FABulous)
- [Caravel HAT](https://github.com/efabless/caravel_board/tree/main/hardware/nucleo/caravel_nucleo)
