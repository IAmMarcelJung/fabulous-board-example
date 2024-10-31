# Uploading the bitstream using the Nucleo board

## TLDR to run the VGA demo

Install [mpremote](https://pypi.org/project/mpremote)
and
[mpy-cross](https://pypi.org/project/mpy-cross/).

Connect a USB cable to `CN1`.

> [!IMPORTANT]
> Be sure to wait a few seconds, until the HAT is fully powered on and
> the Power LED is on. Otherwise, running the bitstream may silently
> fail.

Run this command if the GPIO test process has already been executed and the
firmware has been flashed:

```console
mpremote mount . exec "import fabulous_demo; fabulous_demo.run()"
```

For an empty board without tested GPIOs and flashed firmware:

Follow [this guide](../gpio_test/nucleo_firmware/)
to check the pins for hold time violations.

## Files

This directory contains Bash scripts to load and execute Micropython scripts on
the Nucleo board which are used to upload a bitstream and other data onto the FPGA.
Here is a short description of the files:

- ```copy_and_run_vga_demo.py```: Copy all files needed to run the VGA demo
  without a host PC.
- ```copy_main_for_demo_autostart.sh```: Copy a customized ```main.py``` which
  automatically starts the demo when powering the board.
- ```main.py```: Customized version of ```main.py``` created by the configuration
  scripts. Automatically starts the demo when powering the board.
- ```modules```: Contains Python modules used in the Python scripts.
- ```run.sh```: Run the Python script specified by it's module name over the
  command line.
- ```street.bin```: Containts the images data for the VGA demo.
- ```upload_bitstream_esp.py```: Python script to upload a bitstream using an ESP32
instead of a Nucleo board.
- ```upload_bitstream.py```: Python script to upload the bitstream using the
  Nucleo board.
- ```upload_vga_demo.py```: Python script to upload the bitstream and the image
  using the Nucleo board.

Make sure you have the correct bitstream inside ```../output_files/```.
The bitstream will always be copied into this directory and removed after it
is loaded onto the FPGA. Consider using a symbolic link to your project's
bitstream. It has be located in ```../output_files``` and named
```bitstream.bin```.

## Prerequisites for using the Nucleo board

The upload process is based on micropython modules, so you
need to install [mpremote](https://pypi.org/project/mpremote)
to communicate with the Nucleo board.
To be able to compile your own
micropython file, also install [mpy-cross](https://pypi.org/project/mpy-cross/),
but this is not needed if the board is already prepared for the demo.
If you do not have a bitstream yet, you first have to generate it
using [FABulous](https://github.com/FPGA-Research-Manchester/FABulous).
Make sure to use the `top_wrapper.v` module in `user_design`.

## Hardware

The host PC has to be connected over the ST-LINK USB Micro-B connector  `CN1`
to the Nucleo board.

> [!IMPORTANT]
> Be sure to wait a few seconds until the Nucleo board is powered up.
> Otherwise, running the bitstream may silently fail.

If the GPIOs have not been checked for timing failures for the currently used
part, you have to follow [this guide](./gpio_test/nucleo_firmware/) first.

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

To run the demo execute this command:

```console
mpremote mount . exec "import fabulous_demo; fabulous_demo.run()"
```

The demo is not directly displayed correctly, but this
should only last a few seconds, until the image data is loaded into the FPGA.

If you want to upload your own bitstream, place the bitstream in the
`sim/test_design/` directory and set the `DESIGN` environment variable
to your design name (e.g. `sequential_16bit_en`). Also adjust
`caravel_spi.py` to your needs. Then run

```console
mpremote mount . exec "import caravel_spi; caravel_spi.run()"
```

Of course, you can also come up with your own module.
