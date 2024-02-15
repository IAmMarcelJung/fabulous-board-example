#!/usr/bin/env python3
import time

from modules.myspi import SPI, CARAVEL_STREAM_READ, CARAVEL_REG_READ, CARAVEL_REG_WRITE 
from nucleo_api import ProgSupply
from machine import Pin

class Board:
    def __init__(
        self,
        fpga_clk,
        fpga_clksel0,
        fpga_clksel1,
        fpga_sclk,
        fpga_sdata,
        fpga_rx,
        fpga_rxled,
        fpga_rst,
        fpga_wclk,
        fpga_wdata):
        self.fpga_clk = fpga_clk
        self.fpga_clksel0 = fpga_clksel0
        self.fpga_clksel1 = fpga_clksel1
        self.fpga_sclk = fpga_sclk
        self.fpga_sdata = fpga_sdata
        self.fpga_rx = fpga_rx
        self.fpga_rxled = fpga_rxled
        self.fpga_rst = fpga_rst
        self.fpga_wclk = fpga_wclk
        self.fpga_wdata = fpga_wdata
        self.slave = SPI()

    @staticmethod
    def set_voltage(voltage):
        supply = ProgSupply()
        R2 = 360 / ((voltage / 1.25) - 1)
        Rpot = (1 / (1 / R2 - 1 / 5000)) - 500
        P = Rpot / 38.911
        Pval = int(P)

        print('Writing ' + str(Pval) + ' to potentiometer.')
        supply.write_1v8(Pval)
        time.sleep(1)
         
    def startup_sequence(self):
        print("Powering up...")
        # in some cases, you may need to comment or uncomment this line
        #slave.write([CARAVEL_REG_WRITE, 0x0b, 0x01])
        # ------------

        print(" ")
        print("Caravel data:")
        mfg = self.slave.exchange([CARAVEL_STREAM_READ, 0x01], 2)
        print("   mfg        = {:04x}".format(int.from_bytes(mfg, 'big')))

        product = self.slave.exchange([CARAVEL_REG_READ, 0x03], 1)
        print("   product    = {:02x}".format(int.from_bytes(product, 'big')))

        data = self.slave.exchange([CARAVEL_STREAM_READ, 0x04], 4)
        print("   project ID = {:08x}".format(int.from_bytes(data, 'big')))

        # disable HKSPI
        self.slave.write([CARAVEL_REG_WRITE, 0x6f, 0xff])

        data = self.slave.exchange([CARAVEL_STREAM_READ, 0x03], 4)
        print("   disabled ID = {:08x} (should be 00)".format(int.from_bytes(data, 'big')))

        self.slave.__init__(enabled=False)


    def load_bitstream(self):
        # load bitstream, check receive LED
        ctrl_word = 0x0000FAB1
        # make sure we start desynced
        data = bytes(0xFF for _ in range(128))
        #last_rxled = self.fpga_rxled.value()
        with open("counter.bin", mode='rb') as f:
            data += f.read()
        for i, byte in enumerate(data):
            for j in range(8):
                self.fpga_sdata.value((byte >> (7-j)) & 0x1)
                #last_rxled = self._tog_clk(last_rxled)
                self.fpga_sclk.value(1)
                #last_rxled = self._tog_clk(last_rxled)
                self.fpga_sdata.value((ctrl_word >> (31-(8*(i%4) + j))) & 0x1)
                #last_rxled = self._tog_clk(last_rxled)
                self.fpga_sclk.value(0)
                #last_rxled = self._tog_clk(last_rxled)
            if (i % 100) == 0:
                print("{}".format(i))

    def _tog_clk(self, last_rxled):
        for _ in range(4):
            self.fpga_clk.value(0)
            self.fpga_clk.value(1)
            if self.fpga_rxled.value() != last_rxled:
               print("fpga_rxled: {}".format(self.fpga_rxled.value()))
               last_rxled = self.fpga_rxled.value()
        return last_rxled
