#!/usr/bin/env python3
import time

from modules.myspi import (
    SPI,
    SPIError,
    CARAVEL_STREAM_READ,
    CARAVEL_REG_READ,
    CARAVEL_REG_WRITE,
    CARAVEL_SPI_REG_MANUFACTURER_ID,
    CARAVEL_SPI_REG_MANUFACTURER_ID_DEFAULT_VALUE,
    CARAVEL_SPI_REG_PRODUCT_ID,
    CARAVEL_SPI_REG_PRODUCT_ID_DEFAULT_VALUE,
    CARAVEL_SPI_REG_USER_PROJECT_ID,
    CARAVEL_SPI_REG_PLL_ENABLE,
    CARAVEL_SPI_REG_PLL_ENABLE_DEFAULT_VALUE,
    CARAVEL_SPI_REG_PLL_BYPASS,
    CARAVEL_SPI_REG_PLL_BYPASS_DEFAULT_VALUE,
    CARAVEL_SPI_REG_CPU_RESET,
    CARAVEL_SPI_REG_CPU_RESET_DEFAULT_VALUE,
    CARAVEL_SPI_REG_DCO_TRIM_0,
    CARAVEL_SPI_REG_DCO_TRIM_DEFAULT_VALUE,
    CARAVEL_SPI_REG_PLL_FEEDBACK_DIVIDER,
    CARAVEL_SPI_REG_PLL_FEEDBACK_DIVIDER_DEFAULT_VALUE,
)
from nucleo_api import ProgSupply
from machine import Pin


class Board:
    def __init__(self, fpga_wclk=None, fpga_wdata=None):
        self.fpga_clk = Pin("IO_7", mode=Pin.OUT, value=0)
        self.fpga_clksel0 = Pin("IO_8", mode=Pin.OUT, value=0)
        self.fpga_clksel1 = Pin("IO_9", mode=Pin.OUT, value=0)
        self.fpga_sclk = Pin("IO_10", mode=Pin.OUT, value=0)
        self.fpga_sdata = Pin("IO_11", mode=Pin.OUT, value=0)
        self.fpga_rx = Pin("IO_12", mode=Pin.OUT, value=1)
        self.fpga_rxled = Pin("IO_13", mode=Pin.IN, pull=0)
        self.fpga_rst = Pin("IO_14", mode=Pin.OUT, value=0)

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

        print("Writing " + str(Pval) + " to potentiometer.")
        supply.write_1v8(Pval)
        time.sleep(1)

    def startup_sequence(self):
        print("Powering up...")
        # in some cases, you may need to comment or uncomment this line
        self.slave.write([CARAVEL_REG_WRITE, CARAVEL_SPI_REG_CPU_RESET, 0x01])
        # ------------

        print("Sleeping after CPU reset")
        time.sleep(2)

        print(" ")
        print("Caravel data:")
        self._read_print_and_check_reg(
            CARAVEL_SPI_REG_MANUFACTURER_ID,
            2,
            "Manufacturer ID",
            CARAVEL_SPI_REG_MANUFACTURER_ID_DEFAULT_VALUE,
        )
        """
        mfg = self.slave.exchange(
            [CARAVEL_STREAM_READ, CARAVEL_SPI_REG_MANUFACTURER_ID], 2
        )
        print("   mfg        = {:04x}".format(int.from_bytes(mfg, "big")))

        self._check_retval(mfg, 0x456)
        """
        self._read_print_and_check_reg(
            CARAVEL_SPI_REG_PRODUCT_ID,
            1,
            "Product ID",
            CARAVEL_SPI_REG_PRODUCT_ID_DEFAULT_VALUE,
        )

        """
        product = self.slave.exchange(
            [CARAVEL_REG_READ, CARAVEL_SPI_REG_PRODUCT_ID],
            1,
        )
        print("   product    = {:02x}".format(int.from_bytes(product, "big")))
        self._check_retval(product, 0x10)
        """

        self._read_print_and_check_reg(
            CARAVEL_SPI_REG_USER_PROJECT_ID, 4, "User project ID", None
        )

        """
        data = self.slave.exchange(
            [CARAVEL_STREAM_READ, CARAVEL_SPI_REG_USER_PROJECT_ID], 4
        )

        print("   project ID = {:08x}".format(int.from_bytes(data, "big")))
        data = int.from_bytes(data, "big")
        self._check_retval(mfg, 0x10)
        """

        # disable HKSPI
        self.slave.write([CARAVEL_REG_WRITE, 0x6F, 0xFF])

        self._read_print_and_check_reg(
            CARAVEL_SPI_REG_PRODUCT_ID,
            1,
            "Product ID",
            CARAVEL_SPI_REG_PRODUCT_ID_DEFAULT_VALUE,
        )

        """
        data = self.slave.exchange(
            [CARAVEL_REG_READ, CARAVEL_SPI_REG_PRODUCT_ID],
            1,
        )

        data = int.from_bytes(data, "big")
        print(f"   disabled ID = {data}")
        self._check_retval(data, 0x00)
        """
        self._read_print_and_check_reg(
            CARAVEL_SPI_REG_PLL_ENABLE,
            1,
            "PLL enable",
            CARAVEL_SPI_REG_PLL_ENABLE_DEFAULT_VALUE,
        )

        """
        data = self.slave.exchange([CARAVEL_REG_READ, CARAVEL_SPI_REG_PLL_ENABLE], 1)
        data = int.from_bytes(data, "big")
        print(f"   PLL enable {data}")
        self._check_retval(data, 0x02)
        """
        self._read_print_and_check_reg(
            CARAVEL_SPI_REG_PLL_BYPASS,
            1,
            "PLL bypass",
            CARAVEL_SPI_REG_PLL_BYPASS_DEFAULT_VALUE,
        )

        """
        data = self.slave.exchange([CARAVEL_REG_READ, CARAVEL_SPI_REG_PLL_BYPASS], 1)
        data = int.from_bytes(data, "big")
        print(f"   PLL bypass {data}")
        self._check_retval(data, 0x01)
        """
        self._read_print_and_check_reg(
            CARAVEL_SPI_REG_DCO_TRIM_0,
            1,
            "DCO trim",
            CARAVEL_SPI_REG_DCO_TRIM_DEFAULT_VALUE,
        )

        """
        data = self.slave.exchange([CARAVEL_STREAM_READ, CARAVEL_SPI_REG_DCO_TRIM_0], 1)
        data = int.from_bytes(data, "big")
        print(f"   DCO trim {data}")
        self._check_retval(data, 0x3FFEFFF)
        """

        self._read_print_and_check_reg(
            CARAVEL_SPI_REG_PLL_FEEDBACK_DIVIDER,
            1,
            "PLL feedback divider",
            CARAVEL_SPI_REG_PLL_FEEDBACK_DIVIDER_DEFAULT_VALUE,
        )

        """
        data = self.slave.exchange(
            [CARAVEL_REG_READ, CARAVEL_SPI_REG_PLL_FEEDBACK_DIVIDER], 1
        )
        data = int.from_bytes(data, "big")
        print(f"   PLL feedback divider {data} (should be 0x04)")
        self._check_retval(data, 0x04)
        """

        self.slave.__init__(enabled=False)

    def load_bitstream(self):
        # load bitstream, check receive LED
        ctrl_word = 0x0000FAB1
        # make sure we start desynced
        data = bytes(0xFF for _ in range(128))
        # last_rxled = self.fpga_rxled.value()
        with open("counter.bin", mode="rb") as f:
            data += f.read()
        for i, byte in enumerate(data):
            for j in range(8):
                self.fpga_sdata.value((byte >> (7 - j)) & 0x1)
                # last_rxled = self._tog_clk(last_rxled)
                self.fpga_sclk.value(1)
                # last_rxled = self._tog_clk(last_rxled)
                self.fpga_sdata.value((ctrl_word >> (31 - (8 * (i % 4) + j))) & 0x1)
                # last_rxled = self._tog_clk(last_rxled)
                self.fpga_sclk.value(0)
                # last_rxled = self._tog_clk(last_rxled)
            if (i % 100) == 0:
                print("{}".format(i))

    def load_image_data(self, image):
        for _ in range(2):
            self.fpga_rst.value(1)
            time.sleep(0.01)
            self.fpga_rst.value(0)

            idx = 0
            wclk = False
            with open(image, mode="rb") as f:
                while True:
                    chunk = f.read(256)
                    if len(chunk) == 0:
                        break
                    for j in range(len(chunk) * 8):
                        byte = chunk[j // 8]
                        self.fpga_wdata.value((byte >> (7 - (j % 8)) & 0x1))
                        wclk = not wclk
                        self.fpga_wclk.value(wclk)
                    idx += 1
                    print("wr {}".format(idx))
            time.sleep(2)

    def print_fpga_data(self, n_cycles):
        fpga_data = [Pin("IO_{}".format(i), mode=Pin.IN) for i in range(15, 38)]

        for i in range(n_cycles):
            self.fpga_rst.value(1 if i < 10 else 0)
            self.fpga_clk.value(0)
            time.sleep(0.005)
            self.fpga_clk.value(1)
            b = 0
            for k, p in enumerate(fpga_data):
                if p.value():
                    b |= 1 << k
            print("data: {:023b}".format(b))
            time.sleep(0.005)

    def set_external_clock(self):
        self.fpga_clksel0(0)
        self.fpga_clksel1(0)

    def set_wishbone_clock(self):
        self.fpga_clksel0(1)
        self.fpga_clksel1(0)

    def set_user_clock(self):
        self.fpga_clksel0(1)
        self.fpga_clksel1(1)

    def _tog_clk(self, last_rxled):
        for _ in range(4):
            self.fpga_clk.value(0)
            self.fpga_clk.value(1)
            if self.fpga_rxled.value() != last_rxled:
                print("fpga_rxled: {}".format(self.fpga_rxled.value()))
                last_rxled = self.fpga_rxled.value()
        return last_rxled

    def _check_retval(self, retval, expected):
        if retval not in (expected, None):
            raise SPIError(
                f"Value read from register ({hex(retval)}) did not match the expected value ({hex(expected)})."
            )

    def _read_print_and_check_reg(self, reg, n_bytes, data_name, expected):

        data = 0
        if n_bytes == 0:
            raise ValueError("Need to read at least one byte.")
        elif n_bytes == 1:
            data = self.slave.exchange([CARAVEL_REG_READ, reg], n_bytes)

        else:
            data = self.slave.exchange([CARAVEL_STREAM_READ, reg], n_bytes)
        data = int.from_bytes(data, "big")
        print(f"   {data_name} = {data}")
        # self._check_retval(data, expected)
