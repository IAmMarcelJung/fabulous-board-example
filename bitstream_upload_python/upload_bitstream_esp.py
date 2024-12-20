#!/usr/bin/env python3

import time

from modules.board import Board


def run():
    # Board.set_voltage(1.6)

    board = Board(
        fpga_clk=2,
        fpga_clksel0=4,
        fpga_clksel1=16,
        fpga_sclk=17,
        fpga_sdata=18,
        fpga_rx=19,
        fpga_rxled=21,
        fpga_rst=22,
        kind="esp",
    )

    board.startup_sequence()

    board.set_wishbone_clock()

    board.transmit_bitstream("bitstream.bin")

    print("Sleep for five seconds.")
    time.sleep(5)
    print("Slept for five seconds.")
    board.print_fpga_data(100)
