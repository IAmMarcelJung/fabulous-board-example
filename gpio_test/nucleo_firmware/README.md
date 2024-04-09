# Caravel Nucleo HAT

This directory provides a diagnostic software for characterizing timing failure
patterns between GPIO pads on the Caravel SoC.

This manual is taken from
[the official caravel repository](https://github.com/efabless/caravel_board/tree/main/firmware/mpw2-5/nucleo)
with slight modifications to fit the directory structure of this repository and to
simplify some things. This is also tailored more for anyone working with the
specific FABulous FPGA boards. If you do not have access to those boards you
might rather use the original instructions but also feel free to adapt this to
your needs.

The diagnostic runs on the STM Nucleo board in combination with the Caravel HAT
that hosts the Caravel part under test.

## Setup

### COMPONENTS

- Nucleo-F746ZG or Nucleo-F413ZH
- Caravel HAT
- FABulous FPGA with Caravel
- Two jumpers for J8 & J9
- USB micro-B to USB-A cable

### CONFIGURATION

1. Install the jumpers on J8 and J9 in the `HAT` position to enable the
   board to be powered by the Nucleo.
2. Plug the HAT into the Nucleo board pins
   - The USB on the hat should face the ST-LINK breakoff board on Nucleo and
     away from the push buttons on Nucleo
   - Be careful not to bend a pin when inserting the breakout board.  If one of
     the pins bends, use needle-nose pliers to re-straighten it.

> [!IMPORTANT]
> When pressing the Caravel Hat board on the pin headers of the Nucleo, only
> press far enough to engage the pins. If you press to far, you can short
> the Flexy pins under the board against jumpers on the Nucleo.

> [!NOTE]
> You can also use extension headers to make sure there is both good contact
> to the Nucleo pins and enough clearance for the Flexy Pins.

3. Install a Caravel Breakout board into the HAT's socket, with the
    Efabless logo facing the USB connector on the HAT. If you are using a
    labeled board at Heidelberg University, the logo is covered by the number
    label, so the number label should face the USB connector in the HAT.

4. Connect the USB cable from the connector CN1 on the Nucleo to your
workstation / laptop.

<div align="left" style="margin-left: 30px; margin-bottom: 30px;">
    <img
        src="docs/img/caravel+nucleo_2.jpg"
        alt="A top down view of the Nucleo
        board with the HAT and the Caravel daughterboard installed." width="200"
        title="A top down view of the Nucleo board with the HAT and the Caravel daughterboard installed"./>
    <img
        src="docs/img/nucleo_with_extension_headers.jpeg"
        alt="A side view of the Nucleo
        board showing the extension headers." width="445"
        title="A side view of the Nucleo board showing the extension headers."/>
</div>


### INSTALLATION

1. Install the required tools including `mpremote`, `mpy-cross` and
   `rshell`. The diagnostic runs on a customized Micropython image on the
   Nucleo board.

    - `mpremote` is used for connecting to the MicroPython board.
    - `mpy-cross` is a cross compiler for MicroPython the compiles a python file
      into a binary format which can be run in MicroPython.  It is used here to
      reduce the size of the files because the size of the flash on the Nucleo board
      is limited on some models.

2. You will also need to install the `stlink` tools for your client.
These are required to flash Micropython firmware on the Nucleo board.
See the
[official instructions](https://github.com/stlink-org/stlink/tree/master) on how
to install them on your system.

### FINDING YOUR DEVICE

```bash
  mpremote connect list
```

This will verify you can see the Nucleo board through `mpremote`.  The Makefile
will automatically find and set the device variable.

### UPDATE THE DIAGNOSTIC SOFTWARE

It will be required to update the diagnostic software to get the latest
enhancements and bug fixes.

You can find the model of the Nucleo board on a label in the lower
left corner of the Nucleo board opposite the ST-LINK breakaway board.

Run one of the following make targets based on the model of your Nucleo board:

```bash
make F746ZG
```

```bash
make F413ZH
```

After the flash completes, check the version of the software:

```bash
make version

io_config -- version 1.2.2
```

You only have to run this once for the Nucleo board and then  follow the
instructions in the next section for every different Caravel chip you
are testing.

### RUNNING THE DIAGNOSTIC

> [!NOTE]
> This was already done for some parts in the University Heidelberg, so if you
> have access to those parts you can just use the files inside
> `gpio_config_files` and don't have to run
> the diagnostic. Seven parts have already been tested and label from 0 to 6.

To run the diagnostic, enter the following commands.

The PART variable is an ID for the part you are testing defined by
you. It will be recorded in the output of the test for future reference.
Mark the board under test with the part ID you specified for the run.

```bash
make run PART=<part id>

```

The test will begin with the green LED on the Nucleo flashing 5 times.

If the test completed for the part, run the following to retrieve the
configuration file. The file will indicated the IO that were successfully
checked for either a dependent or independent hold time violation.
Successfully checked IO can be used for this part for firmware
routines.

```bash
make get_config
```

The file is specific to the part you ran the diagnostic with. Each part will
have a different `gpio_config_def.py` file because the timing failure pattern
will be different for each part.

You can also run the test using different voltages, since the hold time is
affected by the voltage. Set the voltages you want to check in
`run_multiple_voltages.sh` and it will loop through all of them,
automatically copy `gpio_config_def.py` after each run and store the
results in `gpio_config_files/<PART>/`. This requires the `Bash` (but
can be easily adapted for other shells) and by
default checks for 1.45V, 1.6V and 1.8V.

## Using the Configuration File

### RUN A SANITY CHECK

The following will run a sanity check test using the gpio_config_def.py produced
from the diagnostic above.  The `gpio_config_def.py` file is stored from the
`make get_config` run above and local on your desktop.

To run the sanity check:

```bash
make sanity_check FILE=gpio_config_def.py
```

BUILDING YOUR OWN FIRMWARE

The `build_firmware_template` directory
(`fabulous-board-example/gpio_test/build_firmware_template`) provides an example
for creating your own firmware. We recommend to copy this directory as a
template to create your own firmware, as it was done with
`build_custom_firmware`.  After copying the directory, update
`gpio_test` to your firmware name in the Makefile.

You will need to copy the `gpio_config_def.py` for your part into this directory.

Update `gpio_config_io.c` with the correct IO configuration for your project.
Each IO should be set to Management or User mode which defines whether the
output is driven from the Management or User area. The IO can be set to output
or inputs with either pull-down, pull-up or no terminating resistors.

> [!NOTE]
> You will not be able to configure any IO that is defined as `H_UNKNOWN` in
> your `gpio_config_def.py` file.  We recommend setting these IO (as well as any
> other IO you are not using) to `C_DISABLE` in your `gpio_config_io.py` file.

You can check that your IO configuration to ensure that you can achieve the
desired configuration by running `make check` from the project directory. If
the configuration can not be configured for that part, you can try changing the
configuration or switching to a different part that can me configured.

In your main firmware, you need to include `../riscv_firmware_src/defs.h` and
`../gpio_config/gpio_config_io.h` (which is already done in the template).

Before using IO, you need to call `gpio_config_io()`.
Below is a simple example for a firmware file. This already is enough for the
FPGA to run, since you don't need to control any pins of the Caravel Soc.

```c
#include "../defs.h"
#include "../gpio_config/gpio_config_io.c"

int main() {

  # initialization

  configure_io();
}
```
However, in the template firmware, there is also a configuration for the GPIO
pin connected to LED D3 to signalize when the firmware is loaded.

You can flash and run your firmware with the Caravel Hat mounted on the Nucleo
by running:

```bash
make clean flash_nucleo
```

This will rebuild the firmware prior to flashing Caravel through the Nucleo
board.

## Troubleshooting

If you are experiencing issues running the diagnostic, there are a few
recommended items to check.

1. Once installed and powered on, check if your part is warm to the touch.  If
   so, you likely have a short in that part (or your project). If its not in
   the project, try another part.
2. Check voltages for the 3.3V and 1.8V supplies in pins J8 and J9.  They should
   be at 3.3V and 1.6V (or whatever voltage your configured) respectively.
3. Ensure your Caravel Hat board is not pressed too far down on the pins to the
   Nucleo.  If it is, you may short some of Flexy pins underneath the Caravel
   Hat board against jumpers from the Nucleo board.  Carefully pull and ease the
   board up on the pins of the 70 pin male headers on the Nucleo so that the
   female headers are just firmly connecting to the pins.
4. There is a known issue wit IO[0] and IO[1] that prevent them from being used
   by the management SoC as outputs. See errata below.

For further details and issues, please see the
[errata](https://docs.google.com/spreadsheets/d/1oErt0V6cgy-dxL2uRPfLjIaFMlooplvvDTThpU-rZAQ/edit?usp=sharing).

## Software

This is a flowchart that describes the Software.

<img src="docs/img/software_flowchart.png" alt="alt text" style="width:200px;"/>

### Functions used by the software

The software is done in micropython and ran on the nucleo, some of the useful
functions that can be used after running `make repl` and importing `io_config`
are:

- `version` : displays the version of this code
- `run_poweron(v)` : powers on Caravel board using the nucleo, with voltage v
  (default is 1.6)
- `run_change_power(v)` : changes 1V8 power on Caravel board using the nucleo
  with voltage v and without resetting the processor.  This can be used to
  modify the operating power after configuring IO at a different voltage.
- `run_flash_caravel()` : flashes Caravel with firmware.hex on the nucleo
  file system
- `run_sanity_check()` : runs the sanity check on an already existing
  `gpio_config_def.py` file on nucleo file system
- `run(part_name, voltage, analog)` : runs the calibration program, analog is a
  flag that specifies if the project is analog
