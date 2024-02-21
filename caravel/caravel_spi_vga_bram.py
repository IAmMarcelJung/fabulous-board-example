#!/usr/bin/env python3

import time

from machine import Pin
from modules.board import Board


def run():
    # set vcc to 1.8V for better fabric perf
    Board.set_voltage(1.8)

    # pin configuration
    fpga_clk = Pin("IO_7", mode=Pin.OUT, value=0)
    fpga_clksel0 = Pin("IO_8", mode=Pin.OUT, value=0)
    fpga_clksel1 = Pin("IO_9", mode=Pin.OUT, value=0)
    fpga_sclk = Pin("IO_10", mode=Pin.OUT, value=0)
    fpga_sdata = Pin("IO_11", mode=Pin.OUT, value=0)
    fpga_rx = Pin("IO_12", mode=Pin.OUT, value=1)
    fpga_rxled = Pin("IO_13", mode=Pin.IN, pull=0)
    fpga_rst = Pin("IO_14", mode=Pin.OUT, value=0)

    fpga_wclk = Pin("IO_20", mode=Pin.OUT, value=0)
    fpga_wdata = Pin("IO_21", mode=Pin.OUT, value=0)

    board = Board(
        fpga_clk,
        fpga_clksel0,
        fpga_clksel1,
        fpga_sclk,
        fpga_sdata,
        fpga_rst,
        fpga_rx,
        fpga_rxled,
        fpga_wclk,
        fpga_wdata,
    )

    board.startup_sequence()

    # use fast clock for configuration
    board.set_fast_clock()

    board.load_bitstream()

    print("Sleeping for 5 seconds.")
    time.sleep(5)
    board.load_image_data("nya.bin")
    # board.print_fpga_data()
