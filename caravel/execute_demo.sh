#!/usr/bin/env bash
set -ex

mpremote connect ${DEV} exec "import caravel_spi_vga_bram; caravel_spi_vga_bram.run()"
