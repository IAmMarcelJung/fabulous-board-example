#!/usr/bin/env python3

import time

from modules.board import Board
from modules.myspi import SPI


def run():
    Board.set_voltage(1.6)

    board = Board()

    board.startup_sequence()

    # use external clock for configuration
    board.set_wishbone_clock()
    # board.set_external_clock()

    board.load_bitstream()
    board.reset_user_logic()

    print("Sleep for one second.")
    time.sleep(1)
    board.print_fpga_data(100)
