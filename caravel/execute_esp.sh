#!/usr/bin/env bash
set -ex

mpremote connect ${ESP_DEV} exec "import caravel_esp; caravel_esp.run()"
