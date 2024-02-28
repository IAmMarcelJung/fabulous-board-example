#!/usr/bin/env python3

import time

from machine import Pin
from modules.board import Board


def run():
    # set vcc to 1.8V for better fabric perf
    Board.set_voltage(1.8)

    # pin configuration
    fpga_wclk = Pin("IO_20", mode=Pin.OUT, value=0)
    fpga_wdata = Pin("IO_21", mode=Pin.OUT, value=0)

    board = Board(
        fpga_wclk,
        fpga_wdata,
    )

    board.startup_sequence()

    # use wishbone clock for configuration
    board.set_wishbone_clock()

    board.load_bitstream()

    print("Sleeping for 5 seconds.")
    time.sleep(5)
    board.load_image_data("nya.bin")
