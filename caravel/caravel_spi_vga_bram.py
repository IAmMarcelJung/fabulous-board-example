#!/usr/bin/env python3

import time

from machine import Pin, soft_reset
from modules.board import Board
from modules.myspi import SPI

def load_image_data(board):
    for _ in range(5):
        board.fpga_rst.value(1)
        time.sleep(0.01)
        board.fpga_rst.value(0)

        idx = 0
        wclk = False
        with open("nya.bin", mode='rb') as f:
            while True:
                chunk = f.read(256)
                if len(chunk) == 0:
                    break
                for j in range(len(chunk)*8):
                    byte = chunk[j//8]
                    board.fpga_wdata.value((byte >> (7-(j % 8)) & 0x1))
                    wclk = not wclk
                    board.fpga_wclk.value(wclk)
                idx += 1
                print("wr {}".format(idx))
        time.sleep(2)

def print_fpga_data(board):
    fpga_data = [Pin('IO_{}'.format(i), mode=Pin.IN) for i in range(15, 38)]

    for i in range(1000):
        board.fpga_rst.value(1 if i < 10 else 0)
        board.fpga_clk.value(0)
        board.fpga_clk.value(1)
        b = 0
        for k, p in enumerate(fpga_data):
            if p.value():
                b |= (1 << k)
        print("data: {:023b}".format(b))
        time.sleep(0.01)

def run():
    # set vcc to 1.8V for better fabric perf
    Board.set_voltage(1.8)

    # pin configuration
    fpga_clk = Pin('IO_7', mode=Pin.OUT, value=0)
    fpga_clksel0 = Pin('IO_8', mode=Pin.OUT, value=0)
    fpga_clksel1 = Pin('IO_9', mode=Pin.OUT, value=0)
    fpga_sclk = Pin('IO_10', mode=Pin.OUT, value=0)
    fpga_sdata = Pin('IO_11', mode=Pin.OUT, value=0)
    fpga_rx = Pin('IO_12', mode=Pin.OUT, value=1)
    fpga_rxled = Pin('IO_13', mode=Pin.IN, pull=0)
    fpga_rst = Pin('IO_14', mode=Pin.OUT, value=0)

    fpga_wclk = Pin('IO_20', mode=Pin.OUT, value=0)
    fpga_wdata = Pin('IO_21', mode=Pin.OUT, value=0)

    board = Board(fpga_clk,
                fpga_clksel0,
                fpga_clksel1,
                fpga_sclk,
                fpga_sdata,
                fpga_rx,
                fpga_rxled,
                fpga_rst,
                fpga_wclk,
                fpga_wdata)

    board.startup_sequence()


    # use fast clock for configuration
    board.fpga_clksel0.value(1)
    board.fpga_clksel1.value(0)

    board.load_bitstream()

    print("Sleeping for 5 seconds.")
    time.sleep(5)
    load_image_data(board)
    print_fpga_data(board)
