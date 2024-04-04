#!/usr/bin/env python3

import time

from machine import Pin
from modules.board import Board


def run():
    Board.set_voltage(1.6)

    board = Board()

    board.startup_sequence()

    # use wishbone clock for configuration
    board.set_wishbone_clock()

    board.load_bitstream()

    board.set_external_clock()

    print("Sleep for one second.")
    time.sleep(1)
    # board.print_fpga_data(100)
    board.run_check_io(10)
