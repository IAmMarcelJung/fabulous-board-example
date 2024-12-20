#!/usr/bin/env python3

from machine import Pin
from modules.board import Board


def run():
    # Set VCC to 1.8V for better fabric perf
    Board.set_voltage(1.8)

    # Pin configuration
    # NOTE: change these depending on you user design
    fpga_wclk = Pin("IO_20", mode=Pin.OUT, value=0)
    fpga_wdata = Pin("IO_21", mode=Pin.OUT, value=0)

    board = Board(
        fpga_wclk=fpga_wclk,
        fpga_wdata=fpga_wdata,
    )

    board.startup_sequence()

    board.set_wishbone_clock()

    board.transmit_bitstream("bitstream.bin")

    for _ in range(5):
        board.load_image_data("street.bin")
