# These need to be defined before including the Makefile
# to set the values defined here in the included Makefile
PATTERN := custom_firmware
FIRMWARE_FILE ?= $(PATTERN).hex
include ../nucleo_firmware/Makefile

VOLTAGE=$(shell python3 -c "from gpio_config_def import voltage; print(voltage)")

GPIO_CONFIG_DATA := ../gpio_config/gpio_config_data.h

gen_config_header: $(GPIO_CONFIG_DATA)

$(GPIO_CONFIG_DATA): gpio_config_def.py gpio_config_io.py
	python3 ../gpio_config/gpio_config_builder.py
	mv gpio_config_data.h $(GPIO_CONFIG_DATA)

check: gpio_config_def.py gpio_config_io.py gpio_config_data.h
	python3 ../gpio_config/gpio_config_checker.py

%.bin: %.elf
	$(TOOLCHAIN_PATH)$(TOOLCHAIN_PREFIX)-objcopy -O binary $< $@

flash_nucleo: gen_config_header custom_firmware.hex flash
	@echo "Finished flashing nucleo."

auto_check_and_flash: check_part F746ZG run get_config gen_config_header check flash_nucleo
	@echo "Finished automatic checking and flashing."

auto_flash: check_part gen_config_header flash_nucleo
	@echo "Finished automatic checking and flashing."


clean::
	rm -f *.hex *.bin *.vvp *.orig $(GPIO_CONFIG_DATA)

.PHONY: clean hex all flash gen_config_header
