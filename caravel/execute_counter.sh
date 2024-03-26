#!/usr/bin/env bash
set -ex

sync
mpremote connect ${DEV} exec "import caravel_spi; caravel_spi.run()"
