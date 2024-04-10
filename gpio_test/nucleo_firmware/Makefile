# Definitions used for device interaction
FLASH := /pyboard/flash/
DEV := $(shell mpremote connect list | grep STLink | cut -f 1 -d ' ')
COPY_CMD :=rshell --port $(DEV) cp
LS_CMD := rshell --port $(DEV) ls

# Definitions related to firmware creation
INCLUDES :=-I$(shell pwd) -I../ -I../generated/ -I../riscv_firmware_src/ -I./src/
TOOLCHAIN_PREFIX :=riscv64-unknown-elf
PATTERN ?= config_io_o

# Definitions related to the GPIO config
CONFIG_FILES_DIR := $(CWD)gpio_config_files
VOLTAGE_STR := $(subst .,_,$(VOLTAGE))
CONFIG_FILE_PATTERN := gpio_config_def
PART_OUTPUT_FILE := $(CONFIG_FILE_PATTERN)_$(PART)_$(VOLTAGE_STR)_V.py
PART_OUTPUT_DIR := part_$(PART)
CONFIG_FILE_TARGET = $(CONFIG_FILES_DIR)/$(PART_OUTPUT_DIR)/$(PART_OUTPUT_FILE)

# Definitions related to python
PYTHON_SRC := $(CWD)src/
PYTHON_FILES := $(wildcard $(PYTHON_SRC)*.py)
MPY_FILES := $(patsubst $(PYTHON_SRC)%.py,$(PYTHON_SRC)%.mpy,$(PYTHON_FILES))

# General defintions
SED_CMD :=sed -i'.orig' -e
CWD := $(dir $(lastword $(MAKEFILE_LIST)))

compile: $(MPY_FILES)

$(PYTHON_SRC)%.mpy: $(PYTHON_SRC)%.py
	mpy-cross $<

# runs script from the local filesystem
reset: check_device
	mpremote connect $(DEV) exec "import machine; machine.reset()"

# runs script from the local filesystem
version: check_device
	mpremote connect $(DEV) exec "import io_config; io_config.version()"

# run io_config test to characterize a new part
run: check_device check_part hex F746ZG-copy
	mpremote connect $(DEV) exec "import io_config; io_config.run('$(PART)', $(VOLTAGE))"

# copy the definition file for a part after running io_config
get_config: check_device
	mpremote cp :$(CONFIG_FILE_PATTERN).py .

# run a sanity check using the gpio_config_def.py file on the nucleo
sanity_check: check_device hex
ifndef CONFIG_FILE
	$(error CONFIG_FILE is undefined, please export it before running make flash)
else
	$(COPY_CMD) $(CONFIG_FILE) $(FLASH)/$(CONFIG_FILE_PATTERN).py
	$(COPY_CMD) $(CWD)config_io_o.hex $(FLASH)
	sync
	sleep 2
	mpremote connect $(DEV) exec "import io_config; io_config.run_sanity_check()"
	mpremote rm :config_io_o.hex
endif

# power up the caravel hat while mounted to Nucleo
poweron: check_device
	mpremote connect $(DEV) exec "import io_config; io_config.run_poweron($(VOLTAGE))"

change_power: check_device check_voltage
	mpremote connect $(DEV) exec "import io_config; io_config.run_change_power($(VOLTAGE))"

# flash firmware on caravel hat while mounted to Nucleo
flash: check_device
ifndef FIRMWARE_FILE
	$(error FIRMWARE_FILE is undefined, please export it before running make flash)
else
	$(COPY_CMD) $(FIRMWARE_FILE) $(FLASH)/firmware.hex
	sync
	sleep 2
	mpremote connect $(DEV) exec "import io_config; io_config.run_flash_caravel()"
	# firmware will be written into the SPI flash and is not needed on the Nucleo flash anymore
	mpremote rm :firmware.hex
endif

# enter repl on nucleo
repl:
	mpremote connect $(DEV) repl

# flash micropython firmware image.  this firmware image has been rebuilt to add pins for the Caravel Nucleo HAT
F746ZG: compile
	st-flash --connect-under-reset --format ihex write $(CWD)F746ZG_firmware.hex
	make F746ZG-copy

F413ZH:
	st-flash --connect-under-reset --format ihex write $(CWD)F413ZH_firmware.hex
	sleep 7
	make F413ZH-copy

# copies scripts to nucleo
copy2 F746ZG-copy: compile check_device hex
	$(COPY_CMD) $(filter-out $(PYTHON_SRC)main.mpy, $(wildcard $(PYTHON_SRC)*.mpy)) $(FLASH)
	$(COPY_CMD) $(PYTHON_SRC)/main.py $(FLASH)
	$(COPY_CMD) $(CWD)config_io_o.hex $(FLASH)
	sync
	$(LS_CMD) $(FLASH)
	echo "File sytem usage"
	mpremote df

copy3 F413ZH-copy: compile check_device hex
	$(COPY_CMD) $(filter-out $(PYTHON_SRC)main.mpy, $(wildcard $(PYTHON_SRC)*.mpy)) $(FLASH)
	$(COPY_CMD) $(PYTHON_SRC)main.py $(FLASH)
	$(COPY_CMD) $(CWD)config_io_o.hex $(FLASH)
	sync
	$(LS_CMD)
	echo "File sytem usage"
	mpremote df

check_device:
ifndef DEV
	$(error "Nucleo device file not found")
endif

check_part:
ifndef PART
	$(error "PART not defined.  Please use 'make run PART=<part_id>'")
endif

check_voltage:
ifndef VOLTAGE
	$(error "VOLTAGE not defined.  Please use 'make change_power VOLTAGE=<voltage>'")
endif

check-python:
ifeq ($(shell which python3),)
$(error Please install python 3.6+)
endif

setup: check-python
	python3 -m pip install rshell
	python3 -m pip install mpy-cross
	python3 -m pip install mpremote

.SUFFIXES:

hex: $(PATTERN:=.hex)

%.elf: %.c $(CWD)../riscv_firmware_src/sections.lds $(CWD)../riscv_firmware_src/crt0_vex.S
	$(TOOLCHAIN_PATH)$(TOOLCHAIN_PREFIX)-gcc $(INCLUDES) -O0 -mabi=ilp32 -march=rv32i -D__vexriscv__ -Wl,-Bstatic,-T,$(CWD)../riscv_firmware_src/sections.lds,--strip-debug -ffreestanding -nostdlib -o $@ $(CWD)../riscv_firmware_src/crt0_vex.S $(CWD)../riscv_firmware_src/isr.c  $(CWD)../gpio_config/gpio_config_io.c $(CWD)src/send_packet.c $<

%.hex: %.elf
	$(TOOLCHAIN_PATH)$(TOOLCHAIN_PREFIX)-objcopy -O verilog $< $@
	$(SED_CMD) 's/@1000/@0000/g' $@
	$(SED_CMD) '1,/@00/!d' $@

$(CONFIG_FILE_TARGET): | run get_config $(CWD)$(CONFIG_FILES_DIR)/$(PART_OUTPUT_DIR)
	cp $(CONFIG_FILE_PATTERN).py $(CWD)$(CONFIG_FILES_DIR)/$(PART_OUTPUT_DIR)/$(PART_OUTPUT_FILE)

$(CONFIG_FILES_DIR)/$(PART_OUTPUT_DIR):
	mkdir -p $@

run_and_get_config: $(CONFIG_FILE_TARGET)
	@echo "Executed GPIO test and stored config file to $(CWD)$(CONFIG_FILE_TARGET)"

clean::
	rm -f *.elf $(PYTHON_SRC)*.mpy *.orig config_io_o.hex

.PHONY: clean hex copy repl run
