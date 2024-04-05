# Set the prefix for `riscvXX-unknown-elf-*`
# On installations using `multilib`, this will be `riscv64` even for compiling to 32-bit targets
TOOLCHAIN_PREFIX=riscv64
#TOOLCHAIN_PREFIX=riscv32
INCLUDES=-I$(shell pwd) -I../ -I../generated/ -I../riscv_firmware_src/ -I../calibration/

#VOLTAGE=$(shell python3 -c "from gpio_config_def import voltage; print(voltage)")
VOLTAGE=1.6

.SUFFIXES:

PATTERN = custom_firmware

hex: ${PATTERN:=.hex}

gpio_config_data.h: gpio_config_def.py gpio_config_io.py
	python3 ../gpio_config/gpio_config_builder.py
	mv gpio_config_data.h ../gpio_config/gpio_config_data.h

check: gpio_config_def.py gpio_config_io.py gpio_config_data.h
	python3 ../gpio_config/gpio_config_checker.py

%.elf: %.c ../riscv_firmware_src/sections.lds ../riscv_firmware_src/crt0_vex.S gpio_config_data.h
	$(TOOLCHAIN_PATH)$(TOOLCHAIN_PREFIX)-unknown-elf-gcc $(INCLUDES) -O0 -mabi=ilp32 -march=rv32i -D__vexriscv__ -Wl,-Bstatic,-T,../riscv_firmware_src/sections.lds,--strip-debug -ffreestanding -nostdlib -o $@ ../riscv_firmware_src/crt0_vex.S ../riscv_firmware_src/isr.c  ../calibration/runtime.c ../gpio_config/gpio_config_io.c $<

%.hex: %.elf
	$(TOOLCHAIN_PATH)$(TOOLCHAIN_PREFIX)-unknown-elf-objcopy -O verilog $< $@
	sed -i.orig -e 's/@1000/@0000/g' $@

%.bin: %.elf
	$(TOOLCHAIN_PATH)$(TOOLCHAIN_PREFIX)-unknown-elf-objcopy -O binary $< $@

flash_nucleo: custom_firmware.hex
	make -f ../nucleo_firmware/Makefile flash FILE=custom_firmware.hex VOLTAGE=$(VOLTAGE)

sanity_check: gpio_config_def.py
	make -f ../nucleo_firmware/Makefile sanity_check FILE=gpio_config_def.py

# run to bringup Caravel power while mounted on Nucleo
poweron:
	make -f ../nucleo_firmware/Makefile poweron VOLTAGE=$(VOLTAGE)

change_power:
	make -f ../nucleo_firmware/Makefile change_power VOLTAGE=$(VOLTAGE)

clean:
	rm -f *.elf *.hex *.bin *.vvp *.orig gpio_config_data.*

.PHONY: clean hex all flash

