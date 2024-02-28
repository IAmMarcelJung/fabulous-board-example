#!/usr/bin/env python3

import time

from machine import Pin
from modules.board import Board


def run():
    Board.set_voltage(1.8)

    board = Board()

    board.startup_sequence()

    # use external clock for configuration
    board.set_wishbone_clock()
    board.set_external_clock()

    board.load_bitstream()

    print("Sleep for five seconds.")
    time.sleep(5)
    board.print_fpga_data(1000)
