# Caravel board scripts

This directory contains Bash scripts to load and execute Micropython scripts on
the Nucleo board which are used to upload a bitstream and other data onto the FPGA.
Here is a short description of the files:

- ```check_io.py```: Run a check to see if the IO configuration worked on all
  pins. Requires a suitable bitstream.
- ```copy_and_run_vga_demo.py```: Copy all files needed to run the VGA demo
  without a host PC.
- ```copy_main_for_demo_autostart.sh```: Copy a customized ```main.py``` which
  automatically starts the demo when powering the board.
- ```main.py```: Customized version of ```main.py``` created by the configuration
  scripts. Automatically starts the demo when powering the board.
- ```modules```: Contains Python modules used in the Python scripts.
- ```run.sh```: Run the Python script specified by it's module name over the
  command line.
- ```street.bin```: Containts the images data for the VGA demo.
- ```upload_bitstream_esp.py```: Python script to upload a bitstream using an ESP32
instead of a Nucleo board.
- ```upload_bitstream.py```: Python script to upload the bitstream using the
  Nucleo board.
- ```upload_vga_demo.py```: Python script to upload the bitstream and the image
  using the Nucleo board.

Make sure you have the correct bitstream inside ```../output_files/```.
The bitstream will always be copied into this directory and removed after it
is loaded onto the FPGA. Consider using a symbolic link to your project's
bitstream. It has be located in ```../output_files``` and named
```bitstream.bin```.
