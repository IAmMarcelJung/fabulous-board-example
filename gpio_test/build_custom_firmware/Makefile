# These need to be defined before including the Makefile
# to set the values defined here in the included Makefile
PATTERN := custom_firmware
FIRMWARE_FILE ?= $(PATTERN).hex
GPIO_CONFIG_DATA := $(CWD)../gpio_config/gpio_config_data.h
GEN_CONFIG_HEADER_PREREQUISITE := gen_config_header
DONT_STRIP_HEX_FILE := true
include ../nucleo_firmware/Makefile

check: gpio_config_def.py gpio_config_io.py gen_config_header
	python3 ../gpio_config/gpio_config_checker.py

%.bin: %.elf
	$(TOOLCHAIN_PATH)$(TOOLCHAIN_PREFIX)-objcopy -O binary $< $@

flash_caravel: custom_firmware.hex
	python3 ../util/caravel_hkflash.py  $<

flash_nucleo: gen_config_header custom_firmware.hex flash
	@echo "Finished flashing nucleo."

auto_check_and_flash: check_part F746ZG run get_config gen_config_header check flash_nucleo
	@echo "Finished automatic checking and flashing."

auto_flash: check_part gen_config_header flash_nucleo
	@echo "Finished automatic checking and flashing."

clean::
	rm -f *.hex *.bin *.vvp *.orig $(GPIO_CONFIG_DATA)

.PHONY: clean hex all flash gen_config_header
