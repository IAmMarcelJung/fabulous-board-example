# This needs to be defined before including the Makefile so PATTERN
# does have the value defined here
PATTERN := custom_firmware
include ../nucleo_firmware/Makefile

VOLTAGE=$(shell python3 -c "from gpio_config_def import voltage; print(voltage)")
#VOLTAGE ?= 1.6
FILE ?= $(FIRMWARE_NAME).hex

gpio_config_data.h: gpio_config_def.py gpio_config_io.py
	python3 ../gpio_config/gpio_config_builder.py
	mv gpio_config_data.h ../gpio_config/gpio_config_data.h

check: gpio_config_def.py gpio_config_io.py gpio_config_data.h
	python3 ../gpio_config/gpio_config_checker.py

%.bin: %.elf
	$(TOOLCHAIN_PATH)$(TOOLCHAIN_PREFIX)-objcopy -O binary $< $@

flash_nucleo: custom_firmware.hex flash
	echo "Finished flashing nucleo."

auto: check_part F746ZG run get_config gpio_config_data.h check flash_nucleo
	echo "Finished automatic checking and flashing."

clean::
	rm -f *.hex *.bin *.vvp *.orig gpio_config_data.*

.PHONY: clean hex all flash

