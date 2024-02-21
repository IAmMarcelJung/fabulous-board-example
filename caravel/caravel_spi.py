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

    # use fast clock for configuration
    board.set_fast_clock()

    board.load_bitstream()

    # use slow clock for running
    board.set_slow_clock()

    print("Sleep for five seconds.")
    time.sleep(5)
    board.print_fpga_data()

    """
    used_pins =  [16, 17, 18, 19, 22, 23, 24]
    pin_pos = []
    #for pin in used_pins:
    for pin in range(15, 38):
        print(pin)
        pin_pos.append(pin - 15)

    fpga_data = [Pin('IO_{}'.format(i), mode=Pin.IN) for i in range(15, 38)]
    for i in range(1000):
        fpga_rst.value(1 if i < 10 else 0)
        fpga_clk.value(0)
        cnt_value = ""
        #print(f"{fpga_clk.value()} ",end=" ")

        for pin in pin_pos:
            cnt_value += f"{fpga_data[pin].value()}"
            #cnt_value += f"{pin}: {fpga_data[pin].value()}, "
        cnt_value += "\n"
        print(cnt_value)
    """
    """
        b = 0
        for k, p in enumerate(fpga_data):
            if p.value():
                b |= (1 << k)
        print("data: {:023b}".format(b))
    """

    #    time.sleep(0.01)
    #    fpga_clk.value(1)
