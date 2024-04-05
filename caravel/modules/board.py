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
        fpga_rst="IO_14",
        kind="nucleo",
        fpga_wclk=None,
        fpga_wdata=None,
    ):
        self.fpga_clk = Pin(fpga_clk, mode=Pin.OUT, value=0)
        self.fpga_clksel0 = Pin(fpga_clksel0, mode=Pin.OUT, value=0)
        self.fpga_clksel1 = Pin(fpga_clksel1, mode=Pin.OUT, value=0)
        self.fpga_sclk = Pin(fpga_sclk, mode=Pin.OUT, value=0)
        self.fpga_sdata = Pin(fpga_sdata, mode=Pin.OUT, value=0)
        self.fpga_rx = Pin(fpga_rx, mode=Pin.OUT, value=1)
        self.fpga_rxled = Pin(fpga_rxled, mode=Pin.IN, pull=0)
        self.fpga_rst = Pin(fpga_rst, mode=Pin.OUT, value=0)

        self.fpga_wclk = fpga_wclk
        self.fpga_wdata = fpga_wdata
        self.kind = kind
        self.slave = MySPI(self.kind)
        self.max_gpio_num = 37
        self.external_clock = False

    @staticmethod
    def set_voltage(voltage):
        from nucleo_api import ProgSupply

        supply = ProgSupply()
        R2 = 360 / ((voltage / 1.25) - 1)
        Rpot = (1 / (1 / R2 - 1 / 5000)) - 500
        P = Rpot / 38.911
        Pval = int(P)

        print("Writing " + str(Pval) + " to potentiometer.")
        supply.write_1v8(Pval)
        time.sleep(1)

    def startup_sequence(self, print_data=False):
        print("Powering up...")
        # CPU reset
        # self.slave.write([CARAVEL_REG_WRITE, CARAVEL_SPI_REG_CPU_RESET, 0x01])
        # print("Sleeping after CPU reset...")
        # time.sleep(1)
        # self.slave.write([CARAVEL_REG_WRITE, CARAVEL_SPI_REG_CPU_RESET, 0x00])
        # print("Sleeping after CPU disable reset...")
        # time.sleep(1)

        # HKSPI disable
        # self.slave.write([CARAVEL_REG_WRITE, CARAVEL_SPI_REG_HKSPI_DISABLE, 0x00])

        # in some cases, you may need to comment or uncomment this line
        # self.slave.write([CARAVEL_REG_WRITE, CARAVEL_SPI_REG_CPU_RESET, 0x00])
        # ------------

        if print_data:
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
        # disable HKSPI

        # self.slave.write([CARAVEL_REG_WRITE, CARAVEL_SPI_REG_HKSPI_DISABLE, 0x00])

        self.slave.__init__(self.kind, enabled=False)

    def bitbang(self, data, ctrl_word):
        self._tog_clk_falling_edge()
        for i, byte in enumerate(data):
            for j in range(8):
                self.fpga_sdata.value((byte >> (7 - j)) & 0x1)
                self.fpga_sclk.value(1)
                self._tog_clk_rising_edge()
                self.fpga_sdata.value((ctrl_word >> (31 - (8 * (i % 4) + j))) & 0x1)
                self.fpga_sclk.value(0)
                self._tog_clk_falling_edge()
            if (i % 100) == 0:
                print("{}".format(i))

    def disable_bitbang(self):
        ctrl_word = 0x0000FAB0
        data = bytes(0)
        self.bitbang(data, ctrl_word)

    def load_bitstream(self, bitstream):
        # load bitstream, check receive LED
        ctrl_word = 0x0000FAB1
        # make sure we start desynced
        data = bytes(0xFF for _ in range(128))
        # last_rxled = self.fpga_rxled.value()
        with open(bitstream, mode="rb") as f:
            data += f.read()
        self.bitbang(data, ctrl_word)

    def load_image_data(self, image):
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

    def print_fpga_data(self, n_cycles):
        if self.kind == "nucleo":
            fpga_data = [
                Pin("IO_{}".format(i), mode=Pin.IN)
                for i in range(15, self.max_gpio_num + 1)
            ]
        else:
            fpga_data = [Pin(i, mode=Pin.IN) for i in range(25, 28)]

        for _ in range(n_cycles):
            # self.fpga_rst.value(1 if i < 10 else 0)
            self.fpga_clk.value(0)
            time.sleep(0.005)
            self.fpga_clk.value(1)
            b = 0
            for k, p in enumerate(fpga_data):
                if p.value():
                    b |= 1 << k
            print("data: {:023b}".format(b))
            time.sleep(0.005)

    def reset_user_logic(self):
        self.fpga_rst.value(1)
        time.sleep(0.01)
        self.fpga_rst.value(0)

    def set_external_clock(self):
        self.external_clock = True
        self.fpga_clksel0(0)
        self.fpga_clksel1(0)

    def set_wishbone_clock(self):
        self.external_clock = False
        self.fpga_clksel0(1)
        self.fpga_clksel1(0)

    def set_user_clock(self):
        self.external_clock = False
        self.fpga_clksel0(1)
        self.fpga_clksel1(1)

    def check_single_output_pin(self, pin, expected):
        """
        Check if a single output pin matches the expected value.

        :param pin: The pin to be checked.
        :param expected: The expected value.
        """
        failed = False
        actual = Pin(f"IO_{pin}", mode=Pin.IN).value()
        if actual != expected:
            failed = True
            print(f"IO_{pin} failed! Expected {expected}, got {actual}.")
        # else:
        #    print(f"IO_{pin} succeeded")

        return failed

    def run_test_procedure(self, output, inputs):
        """
        Run the following test procedure:
        set all inputs to 0
        check output for 0
        set all inputs to 1
        check output for 0
        set each input to 1 in 3 cycles
        check output for 1

        :param output: The output pin to be checked.
        :param inputs: The input pins to change in the procedure."
        """
        succeeded = True
        if not self.check_test_pattern(output, 0, inputs, [0, 0, 0]):
            succeeded = False
        if not self.check_test_pattern(output, 0, inputs, [1, 1, 1]):
            succeeded = False
        if not self.check_test_pattern(output, 1, inputs, [1, 0, 0]):
            succeeded = False
        if not self.check_test_pattern(output, 1, inputs, [0, 1, 0]):
            succeeded = False
        if not self.check_test_pattern(output, 1, inputs, [0, 0, 1]):
            succeeded = False
        return succeeded

    def check_test_pattern(self, output, expected, inputs, test_pattern):
        succeeded = True
        self._tog_clk(0.1)
        for i, input in enumerate(inputs):
            Pin(f"IO_{input}", mode=Pin.IN, value=test_pattern[i])
        if self.check_single_output_pin(output, expected):
            print(
                f"Failed for pattern [{test_pattern[0]}, {test_pattern[1]}, {test_pattern[2]}]."
            )
            succeeded = False
        return succeeded

    def check_output_pins_after_reset(self, input_pin):
        """
        Check if the output pins have the same value as the input pin.
        A suitable bitstream is need for this to succeed.

        :param input_pin: The input pin which will be ignored here.
        """
        failed = False

        self.fpga_rst.value(1)
        time.sleep(0.01)
        print(f"Checking for 0 after reset:")
        for i in range(15, self.max_gpio_num + 1):
            if i is not input_pin:
                if self.check_single_output_pin(i, 0):
                    failed = True

        self.fpga_rst.value(0)
        time.sleep(0.01)
        return failed

    def run_check_io(self, n_cycles):
        """
        Run n cycles of  test procedure.

        :param n_cycles: The number of cycles to run.
        """

        failed = False
        for n in range(n_cycles):
            print(f"Test run {n}")
            for output in range(15, self.max_gpio_num + 1):
                inputs = []
                for input in range(1, 4):
                    tmp_input = (output + input) % self.max_gpio_num
                    inputs.append(tmp_input)
                if not self.run_test_procedure(output, inputs):
                    failed = True

        if failed:
            print("GPIO test failed.")
        else:
            print("GPIO test succeeded.")

    def _tog_clk(self):
        if self.external_clock:
            self.fpga_clk.value(0)
            self.fpga_clk.value(1)

    def _tog_clk_rising_edge(self):
        if self.external_clock:
            self.fpga_clk.value(0)
            self.fpga_clk.value(1)

    def _tog_clk_falling_edge(self):
        if self.external_clock:
            self.fpga_clk.value(1)
            self.fpga_clk.value(0)

    def _check_retval(self, retval, expected, reg):
        if retval not in (expected, None):
            raise SPIError(
                f"Value read ({hex(retval)}) from register ({reg}) did not match the expected value ({hex(expected)})."
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
        print(f"   {data_name} = {hex(data)}")

        # if reg != CARAVEL_SPI_REG_DCO_TRIM_0:
        #    self._check_retval(data, expected, data_name)
