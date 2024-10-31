# These need to be defined before including the Makefile
# to set the values defined here in the included Makefile
PATTERN := gpio_config_firmware
FIRMWARE_FILE ?= $(PATTERN).hex
BITSTREAM_FILE := $(CWD)../../output_files/bitstream.bin
BITSTREAM_HEADER := $(CWD)../firmware_helpers/bitstream/bistream.h
GPIO_CONFIG_DATA := $(CWD)../gpio_config/gpio_config_data.h
GEN_CONFIG_HEADER_PREREQUISITE := gen_config_header
DONT_STRIP_HEX_FILE := true
BITSTREAM_CONVERSION_COMMAND := bin2header

ifeq (, $(shell which $(BITSTREAM_CONVERSION_COMMAND)))
$(error "$(BITSTREAM_CONVERSION_COMMAND) not installed. Get it from: https://github.com/AntumDeluge/bin2header?tab=readme-ov-file")
endif

include ../nucleo_firmware/Makefile

check: gpio_config_def.py gpio_config_io.py gen_config_header
	@echo
	@echo "Checking GPIO configuration."
	python3 ../gpio_config/gpio_config_checker.py
	@echo "$(GREEN)Done checking GPIO configuration.$(RESET_COLOR)"

gpio_sim: gpio_config_def.py gpio_config_io.py gen_config_header
	@echo
	@echo "Simulating GPIO configuration."
	python3 ../gpio_config/gpio_config_simulator.py

%.bin: %.elf
	$(TOOLCHAIN_PATH)$(TOOLCHAIN_PREFIX)-objcopy -O binary $< $@

flash_caravel: $(FIRMWARE_FILE) hex $(BITSTREAM_HEADER)
	@echo
	@echo "Start flashing Caravel."
	python3 ../util/caravel_hkflash.py  $<
	@echo "$(GREEN)Done flashing Caravel.$(RESET_COLOR)"

flash_nucleo: gen_config_header $(FIRMWARE_FILE) flash
	@echo "$(GREEN)Done flashing nucleo.$(RESET_COLOR)"

auto_check_and_flash: check_part F746ZG run get_config gen_config_header check flash_nucleo
	@echo "$(GREEN)Finished automatic checking and flashing.$(RESET_COLOR)"

auto_flash: check_part gen_config_header flash_nucleo
	@echo "$(GREEN)Finished automatic checking and flashing.$(RESET_COLOR)"

$(BITSTREAM_HEADER):
ifeq ("$(wildcard $(BITSTREAM_FILE))", "")
	@echo "$(RED)Bitstream file $(BITSTREAM_FILE) does not exist. Please create it using FABulous and move it to the correct location or use a symlink.$(RESET_COLOR)"
	exit 1
else
	@echo
	@echo "Convert bitstream from binary to header file"
	$(BITSTREAM_CONVERSION_COMMAND) -o ../firmware_helpers/bitstream/bitstream.h -n bitstream ../../output_files/bitstream.bin
	@echo "$(GREEN)Done converting bitstream from binary to header file.$(RESET_COLOR)"
endif

compile: hex

clean::
	rm -f *.hex *.bin *.vvp *.orig $(GPIO_CONFIG_DATA) $(BITSTREAM_HEADER)

.PHONY: clean hex all flash flash_nucleo flash_caravel gen_config_header compile
