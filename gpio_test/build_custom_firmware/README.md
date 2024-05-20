# Build custom firmware

This directory is used to build the firmware for the caravel SoC to upload the
bitstream to the eFPGA. To flash the caravel board in standalone mode, run:

 ```console
 make flash_caravel PART=$(PART_ID) VOLTAGE=$(VOLTAGE)`
 ```

The part ID and voltage are needed to get the correct `gpio_config_def` file.
The voltage on the board is not affected by this and has to be changed by the
Nucleo board or some other I2C capable board.

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
 make flash_nucleo PART=$(PART_ID) VOLTAGE=$(VOLTAGE)`
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
> The Makefiles are not perfect and there is still much room for improvement.
> Feel free to suggest or implement changes!

## Hardware setup

Since it was not possible to use the wishbone interface due to an error in
`fabric/verilog/eFPGA_v3_top_sky130.v`, the GPIO pins of the SoC have to be
used for uploading the bitstream. Therefore make the following connections using
jumper wires:

- `S_DATA`: `IO 37` -> `IO 11`
- `S_CLK`: `IO 36` -> `IO 10`
- `User logic reset`: `IO 35` -> `IO 14`

If you are operating the HAT in standalone mode, you also have to set the clock
select signals via wire connections. These are the possible configurations:

| IO 8   | IO 9   | clock source        |
|--------|--------|---------------------|
|  GND   |  X     | external (IO 7)     |
|  VCC   |  GND   | wishbone (10 MHz)   |
|  VCC   |  VCC   | user                |

 [^1]: This is not needed when using the Nucleo board and could therefore be deleted in the future
