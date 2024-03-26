#!/bin/bash

SELECTED_PART=$1;
voltages=("1.45" "1.6" "1.8");
part_str="part_$SELECTED_PART"
if [ -z "$SELECTED_PART" ]; then 
    echo "Please specify a part number."

else
    for voltage in "${voltages[@]}"; do
        echo "Starting run for $voltage"
        make run PART=$SELECTED_PART VOLTAGE=$voltage
        make get_config
        voltage_str=$(echo "$voltage" | sed 's/\./_/g')
        mv gpio_config_def.py gpio_config_files/$part_str/gpio_config_def_$part_str"_"$voltage_str"_V.py"
    done
fi

