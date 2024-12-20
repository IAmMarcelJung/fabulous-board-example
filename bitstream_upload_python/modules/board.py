#!/usr/bin/env python3
import time

from modules.myspi import (
    MySPI,
    SPIError,
    CARAVEL_STREAM_READ,
    CARAVEL_REG_READ,
    CARAVEL_REG_WRITE,
    CARAVEL_SPI_REG_MANUFACTURER_ID,
    CARAVEL_SPI_REG_MANUFACTURER_ID_DEFAULT_VALUE,
    CARAVEL_SPI_REG_PRODUCT_ID,
    CARAVEL_SPI_REG_PRODUCT_ID_DEFAULT_VALUE,
    CARAVEL_SPI_REG_USER_PROJECT_ID,
    CARAVEL_SPI_REG_USER_PROJECT_ID_DEFAULT_VALUE,
    CARAVEL_SPI_REG_PLL_ENABLE,
    CARAVEL_SPI_REG_PLL_ENABLE_DEFAULT_VALUE,
    CARAVEL_SPI_REG_PLL_BYPASS,
    CARAVEL_SPI_REG_PLL_BYPASS_DEFAULT_VALUE,
    CARAVEL_SPI_REG_CPU_IRQ,
    CARAVEL_SPI_REG_CPU_IRQ_DEFAULT_VALUE,
    CARAVEL_SPI_REG_CPU_RESET,
    CARAVEL_SPI_REG_CPU_RESET_DEFAULT_VALUE,
    CARAVEL_SPI_REG_DCO_TRIM_0,
    CARAVEL_SPI_REG_DCO_TRIM_DEFAULT_VALUE,
    CARAVEL_SPI_REG_PLL_FEEDBACK_DIVIDER,
    CARAVEL_SPI_REG_PLL_FEEDBACK_DIVIDER_DEFAULT_VALUE,
    CARAVEL_SPI_REG_HKSPI_DISABLE,
    CARAVEL_SPI_REG_HKSPI_DISABLE_DEFAULT_VALUE,
)
from machine import Pin
from nucleo_api import ProgSupply

BITS_IN_BYTE = 8
BITS_IN_WORD = 32
BYTES_IN_WORD = 4


class Board:
    def __init__(
        self,
        fpga_clk="IO_7",
        fpga_clksel0="IO_8",
        fpga_clksel1="IO_9",
        fpga_sclk="IO_10",
        fpga_sdata="IO_11",
        fpga_rx="IO_12",
        fpga_rxled="IO_13",
        fpga_rst="IO_37",
        config_start="IO_13",
        kind="nucleo",
        fpga_wclk=None,
        fpga_wdata=None,
    ):
        self.fpga_clk = Pin(fpga_clk, mode=Pin.OUT, value=0)
        self.fpga_clksel0 = Pin(fpga_clksel0, mode=Pin.OUT, value=0)
        self.fpga_clksel1 = Pin(fpga_clksel1, mode=Pin.OUT, value=0)
        self.fpga_sclk = Pin(fpga_sclk, mode=Pin.OUT, value=0)
        self.fpga_sdata = Pin(fpga_sdata, mode=Pin.OUT, value=0)
        self.fpga_rx = Pin(fpga_rx, mode=Pin.IN, pull=0)
        if config_start != "IO_13":
            self.fpga_rxled = Pin(fpga_rxled, mode=Pin.IN, pull=0)
        else:
            self.fpga_rxled = Pin("IO_18", mode=Pin.IN, pull=0)

        self.fpga_rst = Pin(fpga_rst, mode=Pin.OUT, value=0)
        self.config_start = Pin(config_start, mode=Pin.OUT, value=0)

        self.fpga_wclk = fpga_wclk
        self.fpga_wdata = fpga_wdata
        self.kind = kind
        self.slave = MySPI(self.kind)
        self.max_gpio_num = 37
        self.external_clock = False

    @staticmethod
    def set_voltage(voltage: int) -> None:
        """Set the the core voltage for caravel and the user design.

        :param voltage: The core voltage to be set for caravel and the user
        design.
        :type voltage: int
        """

        supply = ProgSupply()
        R2 = 360 / ((voltage / 1.25) - 1)
        Rpot = (1 / (1 / R2 - 1 / 5000)) - 500
        P = Rpot / 38.911
        Pval = int(P)

        print("Writing " + str(Pval) + " to potentiometer.")
        supply.write_1v8(Pval)
        time.sleep(1)

    def startup_sequence(self, check_and_print_data=False):
        """The startup sequence to which checks the Caravel registers and
        initializes the SPI

        :param check_and_print_data: Flag to show whether to print the data or
        not (Default is False).
        """
        print("Powering up...")

        if check_and_print_data:
            print(" ")
            print("Caravel data:")
            self._read_print_and_check_reg(
                CARAVEL_SPI_REG_MANUFACTURER_ID,
                2,
                "Manufacturer ID",
                CARAVEL_SPI_REG_MANUFACTURER_ID_DEFAULT_VALUE,
            )

            self._read_print_and_check_reg(
                CARAVEL_SPI_REG_PRODUCT_ID,
                1,
                "Product ID",
                CARAVEL_SPI_REG_PRODUCT_ID_DEFAULT_VALUE,
            )

            self._read_print_and_check_reg(
                CARAVEL_SPI_REG_USER_PROJECT_ID,
                4,
                "User project ID",
                CARAVEL_SPI_REG_USER_PROJECT_ID_DEFAULT_VALUE,
            )

            self._read_print_and_check_reg(
                CARAVEL_SPI_REG_PLL_ENABLE,
                1,
                "PLL enable",
                CARAVEL_SPI_REG_PLL_ENABLE_DEFAULT_VALUE,
            )

            self._read_print_and_check_reg(
                CARAVEL_SPI_REG_PLL_BYPASS,
                1,
                "PLL bypass",
                CARAVEL_SPI_REG_PLL_BYPASS_DEFAULT_VALUE,
            )

            self._read_print_and_check_reg(
                CARAVEL_SPI_REG_CPU_IRQ,
                1,
                "CPU_IRQ",
                CARAVEL_SPI_REG_CPU_IRQ_DEFAULT_VALUE,
            )

            self._read_print_and_check_reg(
                CARAVEL_SPI_REG_CPU_RESET,
                1,
                "CPU reset",
                CARAVEL_SPI_REG_CPU_RESET_DEFAULT_VALUE,
            )

            self._read_print_and_check_reg(
                CARAVEL_SPI_REG_DCO_TRIM_0,
                4,
                "DCO trim",
                CARAVEL_SPI_REG_DCO_TRIM_DEFAULT_VALUE,
            )

            self._read_print_and_check_reg(
                CARAVEL_SPI_REG_PLL_FEEDBACK_DIVIDER,
                1,
                "PLL feedback divider",
                CARAVEL_SPI_REG_PLL_FEEDBACK_DIVIDER_DEFAULT_VALUE,
            )

        self.slave.__init__(self.kind, enabled=False)

    def bitbang(self, data: bytes, ctrl_word: int) -> None:
        """Transmit data using a custom bitbang protocol.

        :param data: The data to be transmitted.
        :ctrl_word: The control word to be used for the transmission.
        """
        self._set_clk_falling_edge()
        for byte_pos, byte in enumerate(data):
            for bit_pos in range(BITS_IN_BYTE):
                self.fpga_sdata.value((byte >> ((BITS_IN_BYTE - 1) - bit_pos)) & 0x1)
                self.fpga_sclk.value(1)
                self._set_clk_rising_edge()
                self.fpga_sdata.value(
                    (
                        ctrl_word
                        >> (
                            (BITS_IN_WORD - 1)
                            - (BITS_IN_BYTE * (byte_pos % BYTES_IN_WORD) + bit_pos)
                        )
                    )
                    & 0x1
                )
                self.fpga_sclk.value(0)
                self._set_clk_falling_edge()
            if (byte_pos % 100) == 0:
                print("{}".format(byte_pos))

    def disable_bitbang(self):
        """Disable bitbang by sending the control word FAB0."""
        ctrl_word = 0x0000FAB0
        data = bytes(0)
        self.bitbang(data, ctrl_word)

    def transmit_bitstream(self, bitstream_file: str) -> None:
        """Transmit the bitstream to the FPGA.

        :param bitstream_file: The file containing the bitstream to be transmitted.
        :type bitstream_file:
        """
        # Set the control word to enable bitbang
        ctrl_word = 0x0000FAB1

        # make sure we start desynced
        data = bytes(0xFF for _ in range(128))

        with open(bitstream_file, mode="rb") as f:
            data += f.read()
        self.bitbang(data, ctrl_word)

    def load_image_data(self, image_file: str) -> None:
        """Load the image data onto the FPGA.

        :param image_file: The file containing the image data.
        :type image_file: str
        """
        self.reset_user_logic()

        idx = 0
        wclk = False
        with open(image_file, mode="rb") as f:
            # Read the file in in chunks of 256 bytes
            while True:
                chunk = f.read(256)
                if len(chunk) == 0:
                    break
                for bit_pos in range(len(chunk) * BITS_IN_BYTE):
                    byte = chunk[bit_pos // BITS_IN_BYTE]
                    self.fpga_wdata.value(
                        (byte >> ((BITS_IN_BYTE - 1) - (bit_pos % BITS_IN_BYTE)) & 0x1)
                    )
                    wclk = not wclk
                    self.fpga_wclk.value(wclk)
                idx += 1
                print("wr {}".format(idx))

    def print_fpga_data(self, n_cycles: int) -> None:
        """Print the data read from the FPGA pins.

        :param n_cycles: The number of cycles to print the data.
        :type n_cycles: int
        """
        if self.kind == "nucleo":
            fpga_data = [
                Pin("IO_{}".format(i), mode=Pin.IN)
                for i in range(14, self.max_gpio_num - 3)
            ]
        else:
            fpga_data = [Pin(i, mode=Pin.IN) for i in range(25, 28)]

        for _ in range(n_cycles):
            self.fpga_clk.value(0)
            time.sleep(0.005)
            self.fpga_clk.value(1)
            b = 0
            for k, p in enumerate(fpga_data):
                if p.value():
                    b |= 1 << k
            print("data: {:020b}".format(b))
            time.sleep(0.005)

    def reset_user_logic(self):
        """Reset the user logic by strobing the reset pin

        Reset pin of the user logic has to be the same as set here.
        """
        self.fpga_rst.value(1)
        time.sleep(0.01)
        self.fpga_rst.value(0)
        time.sleep(0.01)

    def set_reset_user_logic_value(self, value):
        self.fpga_rst.value(value)

    def start_gpio_configuring(self):
        """Start the gpio configuration by strobing the associated pin.

        The pin of the user logic has to be the same as set here.
        """
        self.config_start.value(1)
        time.sleep(0.01)
        self.config_start.value(0)

    def set_external_clock(self):
        """Set the clock select inputs so that the external clock is used in the
        FPGA"""
        self.external_clock = True
        self.fpga_clksel0(0)
        self.fpga_clksel1(0)

    def set_wishbone_clock(self):
        """Set the clock select inputs so that the wishbone clock is used in the
        FPGA"""
        self.external_clock = False
        self.fpga_clksel0(1)
        self.fpga_clksel1(0)

    def set_user_clock(self):
        """Set the clock select inputs so that the user clock is used in the
        FPGA"""
        self.external_clock = False
        self.fpga_clksel0(1)
        self.fpga_clksel1(1)

    def _set_clk_rising_edge(self):
        """Set a rising edge on the  fpga clock."""
        if self.external_clock:
            self.fpga_clk.value(0)
            self.fpga_clk.value(1)

    def _set_clk_falling_edge(self):
        """Set a falling edge on the fpga clock."""
        if self.external_clock:
            self.fpga_clk.value(1)
            self.fpga_clk.value(0)

    def _check_retval(self, retval, expected, reg):
        """Check if a return value matches the expected value.

        :param retval: The return value to be checked.
        :type retval:
        """
        if retval not in (expected, None):
            raise SPIError(
                f"Value read ({hex(retval)}) from register ({reg}) did not match the expected value ({hex(expected)})."
            )

    def _read_print_and_check_reg(self, reg, n_bytes, register_name, expected_value):
        """Read, print and check the given register.

        :param reg: The register to be read, printed and checked.
        :type reg: int
        :param n_bytes: The number of bytes to be exchanged.
        :type n_bytes: int
        :param register_name: The name of the register.
        :type register_name: str
        :param expected_value: The expected register value.
        :type expected_value: int
        """
        data = 0
        if n_bytes == 0:
            raise ValueError("Need to read at least one byte.")
        elif n_bytes == 1:
            data = self.slave.exchange([CARAVEL_REG_READ, reg], n_bytes)

        else:
            data = self.slave.exchange([CARAVEL_STREAM_READ, reg], n_bytes)
        data = int.from_bytes(data, "big")
        print(f"   {register_name} = {hex(data)}")

        if reg != CARAVEL_SPI_REG_DCO_TRIM_0:
            self._check_retval(data, expected_value, register_name)
