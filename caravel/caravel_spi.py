#!/usr/bin/env python3

import time

from machine import Pin
from modules.board import Board


def run():
    Board.set_voltage(1.8)

    fpga_clk = Pin("IO_7", mode=Pin.OUT, value=0)
    fpga_clksel0 = Pin("IO_8", mode=Pin.OUT, value=0)
    fpga_clksel1 = Pin("IO_9", mode=Pin.OUT, value=0)
    fpga_sclk = Pin("IO_10", mode=Pin.OUT, value=0)
    fpga_sdata = Pin("IO_11", mode=Pin.OUT, value=0)
    fpga_rst = Pin("IO_14", mode=Pin.OUT, value=0)

    board = Board(fpga_clk, fpga_clksel0, fpga_clksel1, fpga_sclk, fpga_sdata, fpga_rst)

    board.startup_sequence()

    # use external clock for configuration
    board.set_wishbone_clock()

    board.load_bitstream()

    print("Sleep for five seconds.")
    time.sleep(5)
    board.print_fpga_data(100)
