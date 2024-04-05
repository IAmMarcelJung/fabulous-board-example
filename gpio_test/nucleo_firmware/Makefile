FLASH=/pyboard/flash/
DEV=$(shell mpremote connect list | grep STLink | cut -f 1 -d ' ')
COPY_CMD=rshell --port ${DEV} cp
#COPY_CMD=cp
LS_CMD=rshell --port ${DEV} ls
#LS_CMD=ls

# cross compile python to micropython bin.
compile:
	mpy-cross src/flash.py
	mpy-cross src/io_config.py
	mpy-cross src/gpio_config_builder.py
	mpy-cross src/i2c.py
	mpy-cross src/nucleo_api.py
	mpy-cross src/boot.py

# runs script from the local filesystem
reset: check_device
	mpremote connect ${DEV} exec "import machine; machine.reset()"

# runs script from the local filesystem
version: check_device
	mpremote connect ${DEV} exec "import io_config; io_config.version()"

# run io_config test to characterize a new part
run: check_device check_part
	mpremote connect ${DEV} exec "import io_config; io_config.run('$(PART)', $(VOLTAGE))"

run_analog: check_device check_part
ifdef VOLTAGE
	mpremote connect ${DEV} exec "import io_config; io_config.run('$(PART)', voltage=$(VOLTAGE), analog=True)"
else
	mpremote connect ${DEV} exec "import io_config; io_config.run('$(PART)', analog=True)"
endif

# copy the definition file for a part after running io_config
get_config: check_device
	mpremote cp :gpio_config_def.py .

# run a sanity check using the gpio_config_def.py file on the nucleo
sanity_check: check_device
ifndef FILE
	$(error FILE is undefined, please export it before running make flash)
else
	$(COPY_CMD) ${FILE} ${FLASH}/gpio_config_def.py
	sync
	sleep 2
	mpremote connect ${DEV} exec "import io_config; io_config.run_sanity_check()"
endif

# power up the caravel hat while mounted to Nucleo
poweron: check_device
	mpremote connect ${DEV} exec "import io_config; io_config.run_poweron($(VOLTAGE))"

change_power: check_device check_voltage
	mpremote connect ${DEV} exec "import io_config; io_config.run_change_power($(VOLTAGE))"

# flash firmware on caravel hat while mounted to Nucleo
flash: check_device
ifndef FILE
	$(error FILE is undefined, please export it before running make flash)
else
	$(COPY_CMD) ${FILE} ${FLASH}/firmware.hex
	sync
	sleep 2
	mpremote connect ${DEV} exec "import io_config; io_config.run_flash_caravel()"
	# firmware will be written into the SPI flash and is not needed on the Nucleo flash anymore
	mpremote rm :firmware.hex
endif

# enter repl on nucleo
repl:
	mpremote connect ${DEV} repl

# flash micropython firmware image.  this firmware image has been rebuilt to add pins for the Caravel Nucleo HAT
F746ZG: compile
	st-flash --connect-under-reset --format ihex write F746ZG_firmware.hex
	make F746ZG-copy

F413ZH:
	st-flash --connect-under-reset --format ihex write F413ZH_firmware.hex
	sleep 7
	make F413ZH-copy

# copies scripts to nucleo
copy2 F746ZG-copy: compile check_device
	$(COPY_CMD) src/flash.mpy src/i2c.mpy src/gpio_config_builder.mpy src/nucleo_api.mpy src/io_config.mpy ${FLASH}
	$(COPY_CMD) src/main.py ${FLASH}
	sync
	${LS_CMD} ${FLASH}
	echo "File sytem usage"
	mpremote df

copy3 F413ZH-copy: check_device
	$(COPY_CMD) src/flash.mpy src/i2c.mpy src/gpio_config_builder.mpy src/nucleo_api.mpy src/io_config.mpy ${FLASH}
	$(COPY_CMD) src/main.py ${FLASH}
	sync
	${LS_CMD}
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

clean:
	rm -f *.elf

.PHONY: clean image hex copy repl run
