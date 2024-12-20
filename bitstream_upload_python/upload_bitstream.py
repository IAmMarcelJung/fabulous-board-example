#!/usr/bin/env python3

import time

from modules.board import Board


def run():
    """Function to be run on the Nucleo board.

    Needs the correct firmware to be
    operational
    """
    Board.set_voltage(1.6)

    board = Board()

    board.startup_sequence()

    board.set_wishbone_clock()

    board.transmit_bitstream("bitstream.bin")

    board.start_gpio_configuring()

    board.reset_user_logic()

    print("Sleep for ten seconds.")

    time.sleep(10)

    board.print_fpga_data(100)
