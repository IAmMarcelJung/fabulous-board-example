#!/usr/bin/env python3
import time
from machine import Pin, SoftSPI, sleep, SPI

# from nucleo_api import Test


CARAVEL_PASSTHRU = 0xC4
CARAVEL_STREAM_READ = 0x40
CARAVEL_STREAM_WRITE = 0x80
CARAVEL_REG_READ = 0x48
CARAVEL_REG_WRITE = 0x88
CARAVEL_REG_READ2 = 0x50
CARAVEL_REG_WRITE2 = 0x90

CARAVEL_SPI_REG_STATUS = 0x00

CARAVEL_SPI_REG_MANUFACTURER_ID = 0x01
CARAVEL_SPI_REG_MANUFACTURER_ID_DEFAULT_VALUE = 0x456

CARAVEL_SPI_REG_PRODUCT_ID = 0x03
CARAVEL_SPI_REG_PRODUCT_ID_DEFAULT_VALUE = 0x11

CARAVEL_SPI_REG_USER_PROJECT_ID = 0x04
CARAVEL_SPI_REG_USER_PROJECT_ID_DEFAULT_VALUE = 0x00

CARAVEL_SPI_REG_PLL_ENABLE = 0x08
CARAVEL_SPI_REG_PLL_ENABLE_DEFAULT_VALUE = 0x02

CARAVEL_SPI_REG_PLL_BYPASS = 0x09
CARAVEL_SPI_REG_PLL_BYPASS_DEFAULT_VALUE = 0x01

CARAVEL_SPI_REG_CPU_IRQ = 0x0A
CARAVEL_SPI_REG_CPU_IRQ_DEFAULT_VALUE = 0x00

CARAVEL_SPI_REG_CPU_RESET = 0xB
CARAVEL_SPI_REG_CPU_RESET_DEFAULT_VALUE = 0x00

CARAVEL_SPI_REG_CPU_TRAP = 0x0C

CARAVEL_SPI_REG_DCO_TRIM_0 = 0x0D
CARAVEL_SPI_REG_DCO_TRIM_1 = 0x0E
CARAVEL_SPI_REG_DCO_TRIM_2 = 0x0F
CARAVEL_SPI_REG_DCO_TRIM_3 = 0x10

CARAVEL_SPI_REG_DCO_TRIM_0_DEFAULT_VALUE = 0x03
CARAVEL_SPI_REG_DCO_TRIM_1_DEFAULT_VALUE = 0xFF
CARAVEL_SPI_REG_DCO_TRIM_2_DEFAULT_VALUE = 0xEF
CARAVEL_SPI_REG_DCO_TRIM_3_DEFAULT_VALUE = 0xFF
CARAVEL_SPI_REG_DCO_TRIM_DEFAULT_VALUE = 0x3FFEFFF

CARAVEL_SPI_REG_PLL_OUTPUT_DIVIDER = 0x11
CARAVEL_SPI_REG_PLL_OUTPUT_DIVIDER_DEFAULT_VALUE = 0x12

CARAVEL_SPI_REG_PLL_FEEDBACK_DIVIDER = 0x12
CARAVEL_SPI_REG_PLL_FEEDBACK_DIVIDER_DEFAULT_VALUE = 0x04

CARAVEL_SPI_REG_HKSPI_DISABLE = 0x6F
CARAVEL_SPI_REG_HKSPI_DISABLE_DEFAULT_VALUE = 0x00


class SPIError(Exception):
    """An exception to be thrown if the an error occurs during SPI communication."""

    def __init__(self, message=""):
        self.message = message


class MySPI:
    def __init__(self, board="nucleo", enabled=True):
        cs = "SPI5_CS"
        if board == "esp":
            cs = 15
        if enabled:
            self.cs = Pin(cs, mode=Pin.OUT, value=1)
            if board == "nucleo":
                self.sck = Pin("SPI5_SCK", mode=Pin.OUT, value=0)
                self.mosi = Pin(
                    "SPI5_MOSI", mode=Pin.OUT
                )  # PF9 = IO[2] = caravel input
                self.miso = Pin(
                    "SPI5_MISO", mode=Pin.IN
                )  # PF8 = IO[1] = caravel output
                self.spi = SoftSPI(
                    baudrate=4000000,
                    polarity=0,
                    phase=0,
                    sck=self.sck,
                    mosi=self.mosi,
                    miso=self.miso,
                )
            else:
                self.spi = SPI(
                    1,
                    1_000_000,
                )

        else:
            if board == "nucleo":
                self.cs = Pin(cs, mode=Pin.IN, pull=None)
                self.sck = Pin("SPI5_SCK", mode=Pin.IN, pull=None)
                self.mosi = Pin(
                    "SPI5_MISO", mode=Pin.IN, pull=None
                )  # PF9 = IO[2] = caravel input
                self.miso = Pin(
                    "SPI5_MOSI", mode=Pin.IN, pull=None
                )  # PF8 = IO[1] = caravel output
            self.spi = None

    def write(self, buf):
        txdata = bytearray(buf)
        self.cs.value(0)
        self.spi.write(txdata)
        self.cs.value(1)

    def exchange(self, buf, n):

        txdata = bytearray(buf)
        txdata += "\0" * (n)
        m = len(txdata)
        rxdata = bytearray(m)

        self.cs.value(0)
        self.spi.write_readinto(txdata, rxdata)
        self.cs.value(1)
        return rxdata[m - n : m]

    def set_gpio(self, value):
        for i in range(4):
            self.write([CARAVEL_STREAM_WRITE, 0x6D - i, (value >> (8 * i)) & 0xFF])

    def set_mprj_mode(self, io, value):
        self.write([CARAVEL_STREAM_WRITE, 0x1D + 2 * io + 0, (value >> 8) & 0x1F])
        self.write([CARAVEL_STREAM_WRITE, 0x1D + 2 * io + 1, value & 0xFF])

    def yeet_mprj(self):
        self.write([CARAVEL_STREAM_WRITE, 0x13, 1])
        time.sleep(0.1)
