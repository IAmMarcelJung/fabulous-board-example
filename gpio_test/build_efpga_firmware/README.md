# Build eFPGA firmware

This directory is used to build the firmware for the caravel SoC so that the
GPIOs are configured in a way that it is possible to upload the
bitstream to the eFPGA.

## Firmware Files
`gpio_config_firmware_MPW2.c`: Configure the GPIOs fitting for the MPW-2 eFPGA.

`gpio_config_firmware_MPW5.c`: Configure the GPIOs fitting for the MPW-5 eFPGA.

`bitstream_bitbang_upload_firmware.c`: Configure the GPIOs fitting for the MPW-2
and use a [custom bitbang
protocol](https://fabulous.readthedocs.io/en/latest/simulation/simulation.html)
to upload a bitstream. Does not work with MPW-5 eFPGAs and
requires an adjusted `gpio_config_io_MPW2.py` (set IO 36 and 37 to `C_MGMT_OUT`).

`firmware_no_io_config.c`: Does not configure the GPIOs. The default mode
`MGMT_STD_INPUT_NOPULL` is used. This can be helpful for debugging if the GPIO configuration is
faulty. With this configuration, it is always possible to upload a bitstream to
the eFPGA, since the input is always connected to the eFGPA. However, there will
be no output from the eFPGA. By measuring the power draw and a power-intensive
design, it can then be seen if the upload was successful.

`uart_communication_firmware.c`: Communicate with the caravel SoC from a host PC
over UART. Does not configure the GPIOs. The functionality was not tested for some
time, so it could be broken.

To flash the caravel SoC in standalone mode (without the Nucleo board), run:

 ```console
 make flash_caravel PART=$(PART_ID) SHUTTLE=($SHUTTLE) VOLTAGE=$(VOLTAGE)`
 ```

The part ID (e.g. `50`) and voltage are needed to get the correct `gpio_config_def.py` file.
The voltage on the board is not affected by this and has to be changed by the
Nucleo board or some other I2C capable board. Specifying the voltage is
optional, by default files that were created with a voltage of 1.5V will be
used.
The shuttle (`MPW2`/`MPW5`) variable is used to copy the correct
`gpio_config_io.py` file. This is needed since the chips of the MPW-5 run do
have a wrong setting for the `io_oeb` bit.

> [!Note]
> Make sure to connect the wires as specified in the [top level README](../../README.md).

Make will then execute the following steps:

- Convert the bitstream into a header file.
- Copy the `gpio_config_def` file for the specified part and voltage to this directory.
- Build the configuration data for the GPIO configuration.
- Compile the firmware.
- Convert the `.elf` file to a `.hex` file.
- Check the GPIO configuration.
- Flash the firmware.
- Remove the elf file.

You can also run:

 ```console
 make flash_nucleo PART=$(PART_ID) SHUTTLE_$(SHUTTLE) VOLTAGE=$(VOLTAGE)`
 ```

This will upload the firmware using the Nucleo board.

The following steps will be executed:

- Copy the `gpio_config_def` file for the specified part and voltage to this directory.
- Build the configuration data for the GPIO configuration.
- Convert the bitstream into a header file [^1]
- Compile the firmware.
- Convert the `.elf` file to a `.hex` file.
- Copy the firmware to the Nucleo board.
- Run `io_config.run_flash_caravel()` to flash the firmware.
- Remove the elf file.

> [!Note]
> The Makefiles are by far not perfect and there is still much room for improvement.
> Feel free to suggest or implement changes!

## Hardware setup

Since it was not possible to use the wishbone interface due to an error in
`fabric/verilog/eFPGA_v3_top_sky130.v`, the GPIO pins of the SoC have to be
used for uploading the bitstream. Therefore, make the following connections using
jumper wires:

- `S_DATA`: `IO 37` -> `IO 11`
- `S_CLK`: `IO 36` -> `IO 10`
- `User logic reset`: `IO 35` -> `IO 14` (This is optional and depends on the
user design)

It is also possible to use UART to upload a bitstream. The software can be found
[here](https://github.com/IAmMarcelJung/FABulous_board/tree/main/software)

If you are operating the HAT in standalone mode, you also have to set the clock
select signals via wire connections. These are the possible configurations:

| IO 8   | IO 9   | clock source        |
|--------|--------|---------------------|
|  GND   |  X     | external (IO 7)     |
|  VCC   |  GND   | wishbone (10 MHz)   |
|  VCC   |  VCC   | user                |

> [!Note]
> For chips from the MPW-5 shuttle this has no effect, due to the wrong `io_oeb`
> setting.

 [^1]: This is not needed when using the Nucleo board and could therefore be deleted in the future
