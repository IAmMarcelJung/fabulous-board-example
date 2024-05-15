#!/usr/bin/env python3

from pyftdi.ftdi import Ftdi
import time
import sys, os
from pyftdi.spi import SpiController
import binascii
import asyncio
from io import StringIO


SR_WIP = 0b00000001  # Busy/Work-in-progress bit
SR_WEL = 0b00000010  # Write enable bit
SR_BP0 = 0b00000100  # bit protect #0
SR_BP1 = 0b00001000  # bit protect #1
SR_BP2 = 0b00010000  # bit protect #2
SR_BP3 = 0b00100000  # bit protect #3
SR_TBP = SR_BP3  # top-bottom protect bit
SR_SP = 0b01000000
SR_BPL = 0b10000000
SR_PROTECT_NONE = 0  # BP[0..2] = 0
SR_PROTECT_ALL = 0b00011100  # BP[0..2] = 1
SR_LOCK_PROTECT = SR_BPL
SR_UNLOCK_PROTECT = 0
SR_BPL_SHIFT = 2

CMD_READ_STATUS = 0x05  # Read status register
CMD_WRITE_ENABLE = 0x06  # Write enable
CMD_WRITE_DISABLE = 0x04  # Write disable
CMD_PROGRAM_PAGE = 0x02  # Write page
CMD_EWSR = 0x50  # Enable write status register
CMD_WRSR = 0x01  # Write status register
CMD_ERASE_SUBSECTOR = 0x20
CMD_ERASE_HSECTOR = 0x52
CMD_ERASE_SECTOR = 0xD8
CMD_ERASE_CHIP = 0x60
CMD_RESET_CHIP = 0x99
CMD_JEDEC_DATA = 0x9F

CMD_READ_LO_SPEED = 0x03  # Read @ low speed
CMD_READ_HI_SPEED = 0x0B  # Read @ high speed
ADDRESS_WIDTH = 3

JEDEC_ID = 0xEF
SPI_FREQ_MAX = 104  # MHz
CMD_READ_UID = 0x4B
UID_LEN = 0x8  # 64 bits
READ_UID_WIDTH = 4  # 4 dummy bytes

CARAVEL_PASSTHRU = 0xC4
CARAVEL_STREAM_READ = 0x40
CARAVEL_STREAM_WRITE = 0x80
CARAVEL_REG_READ = 0x48
CARAVEL_REG_WRITE = 0x88


class Led:
    def __init__(self, gpio):
        self.gpio = gpio
        self.gpio
        self.led = 1

    def toggle(self):
        """Toggle the led once."""
        self.led = (self.led + 1) & 0x1
        output = 0b000100000000 | self.led << 11
        if self.gpio:
            self.gpio.write(output)
            time.sleep(0.2)

    async def toggle_until_stop_event(self, stop_event):
        """Toggle the led until the stop event is set.

        :param stop_event: The stop event for which to check.
        """
        while not stop_event.is_set():
            await asyncio.to_thread(self.toggle)


class Memory:
    def __init__(self, slave):
        self.slave = slave

    def write_passthrough_command(self, command_id):
        self.slave.write([CARAVEL_PASSTHRU, command_id])

    async def erase(self, stop_event):
        """Erase the flash memory
        :param stop_event: The stop event to set when erasing is done.
        """
        print(" ")
        print("Resetting Flash...")
        self.slave.write([CARAVEL_PASSTHRU, CMD_RESET_CHIP])

        print("status = 0x{:02x}".format(self.get_status(), "02x"))

        print(" ")

        jedec = self.slave.exchange([CARAVEL_PASSTHRU, CMD_JEDEC_DATA], 3)
        print("JEDEC = {}".format(binascii.hexlify(jedec)))

        if jedec[0:1] != bytes.fromhex("ef"):
            print("Winbond flash not found")
            sys.exit()

        print("Erasing chip...")
        self.write_passthrough_command(CMD_WRITE_ENABLE)
        self.write_passthrough_command(CMD_ERASE_CHIP)

        while self.is_busy():
            await asyncio.sleep(0.1)

        print("done")
        print("status = {}".format(hex(self.get_status())))
        stop_event.set()

    def is_busy(self):
        """Get if the memory is busy."""
        return self.get_status() & SR_WIP

    def get_status(self):
        return int.from_bytes(
            self.slave.exchange([CARAVEL_PASSTHRU, CMD_READ_STATUS], 1),
            byteorder="big",
        )

    def mem_action(self, file_path, write):
        if not write:
            print("************************************")
            print("Verifying...")
            print("************************************")
        buf = bytearray()
        addr = 0
        nbytes = 0
        total_bytes = 0

        with open(file_path, mode="r") as f:
            x = f.readline()
            while x != "":
                if x[0] == "@":
                    addr = int(x[1:], 16)
                    print(f"setting address to {hex(addr)}")
                else:
                    values = bytearray.fromhex(x[0 : len(x) - 1])
                    buf[nbytes:nbytes] = values
                    nbytes += len(values)

                x = f.readline()

                if nbytes >= 256 or (x != "" and x[0] == "@" and nbytes > 0):
                    total_bytes += nbytes
                    self.__transfer_sequence(write, nbytes, buf, addr)

                    if nbytes > 256:
                        buf = buf[255:]
                        addr += 256
                        nbytes -= 256
                        print("*** over 256 hit")
                    else:
                        buf = bytearray()
                        addr += 256
                        nbytes = 0

            if nbytes > 0:
                total_bytes += nbytes
                self.__transfer_sequence(write, nbytes, buf, addr)

        print(f"\ntotal_bytes = {total_bytes}")

    def __read_actions(self, read_cmd, nbytes, buf, addr):
        buf2 = self.slave.exchange(read_cmd, nbytes)
        if buf == buf2:
            print(f"addr {hex(addr)}: read compare successful")
        else:
            print("addr {hex(addr)}: *** read compare FAILED ***")
            print(binascii.hexlify(buf))
            print("<----->")
            print(binascii.hexlify(buf2))

    def __write_actions(self, wcmd, buf, addr):
        wcmd.extend(buf)
        self.slave.exchange(wcmd)
        while self.is_busy():
            time.sleep(0.1)

        print(f"addr {hex(addr)}: flash page write successful")

    def __transfer_sequence(self, write, nbytes, buf, addr):
        if write:
            self.slave.write([CARAVEL_PASSTHRU, CMD_WRITE_ENABLE])
            memory_command = CMD_PROGRAM_PAGE
        else:
            memory_command = CMD_READ_LO_SPEED

        cmd = bytearray(
            (
                CARAVEL_PASSTHRU,
                memory_command,
                (addr >> 16) & 0xFF,
                (addr >> 8) & 0xFF,
                addr & 0xFF,
            )
        )
        if write:
            self.__write_actions(cmd, buf, addr)
        else:
            self.__read_actions(cmd, nbytes, buf, addr)


class MyFtdi(Ftdi):
    def __init__(self):
        super().__init__()
        self.device = self.__read_device_url()
        self.spi = SpiController(cs_count=2)
        self.spi.configure(self.device)
        self.slave = self.spi.get_port(cs=0, freq=12e6, mode=0)
        self.led = self.__assign_led_to_gpio()
        self.memory = Memory(self.slave)
        self.mfg_id = bytes(0)

    def enable_cpu_reset(self):
        """Reset the CPU over an SPI command."""
        self.slave.write([CARAVEL_REG_WRITE, 0x0B, 0x01])

    def disable_cpu_reset(self):
        """Reset the CPU over an SPI command."""
        self.slave.write([CARAVEL_REG_WRITE, 0x0B, 0x00])

    def print_manufacturer_and_product_id(self):
        """Print the manufacturer and product ID."""
        print(" ")
        print("Caravel data:")
        self.mfg_id = self.slave.exchange([CARAVEL_STREAM_READ, 0x01], 2)
        print(
            "   Manufacturer ID = {:04x}".format(
                int.from_bytes(self.mfg_id, byteorder="big")
            )
        )

        product = self.slave.exchange([CARAVEL_REG_READ, 0x03], 1)
        print(
            "   Product ID      = {:02x}".format(
                int.from_bytes(product, byteorder="big")
            )
        )

    def check_manufacturer_id(self):
        mfg_int = int.from_bytes(self.mfg_id, byteorder="big")
        if mfg_int != 0x0456:
            print(
                f"Manufacturer ID does not does not match! Expected 0x0456, got {hex(mfg_int)}."
            )
            print(
                "You might want to power cycle the board and start flashing before the firmware configures the GPIOs.\n"
            )
            exit(2)

    def __read_device_url(self):
        """Sets the URL of the connected FTDI device.
        :returns: The device URL of the connected FTDI device.
        :rtype: str
        """

        s = StringIO()
        self.show_devices(out=s)
        devlist = s.getvalue().splitlines()[1:-1]
        ftdi_devices = []
        for dev in devlist:
            url = dev.split("(")[0].strip()
            name = "(" + dev.split("(")[1]
            if name == "(Single RS232-HS)":
                ftdi_devices.append(url)
        if len(ftdi_devices) == 0:
            print("Error: No matching FTDI devices on USB bus!")
            sys.exit(1)
        elif len(ftdi_devices) > 1:
            print("Error: Too many matching FTDI devices on USB bus!")
            self.show_devices()
            sys.exit(1)
        else:
            print("Success: Found one matching FTDI device at " + ftdi_devices[0])
        return ftdi_devices[0]

    def __assign_led_to_gpio(self):
        """Assign the led to the correct gpio."""
        gpio = self.spi.get_gpio()
        gpio.set_direction(0b110100000000, 0b110100000000)  # (mask, dir)
        return Led(gpio)


def get_file_path_from_args(args):
    """Gets the file path from the given command line arguments.

    :param args: The given command line arguments.
    :returns: The file path.
    :rtype: str
    """
    if len(args) < 2:
        print(f"Usage: {os.path.basename(__file__)} <file>")
        sys.exit()

    file_path = args[1]

    if not os.path.isfile(file_path):
        print("File not found.")
        sys.exit()
    return file_path


async def main():
    file_path = get_file_path_from_args(sys.argv)

    ftdi = MyFtdi()
    ftdi.led.toggle()
    ftdi.enable_cpu_reset()
    ftdi.print_manufacturer_and_product_id()
    ftdi.check_manufacturer_id()

    stop_event = asyncio.Event()
    toggle_task = asyncio.create_task(ftdi.led.toggle_until_stop_event(stop_event))
    erase_task = asyncio.create_task(ftdi.memory.erase(stop_event))
    await toggle_task
    await erase_task

    ftdi.memory.mem_action(file_path, True)

    while ftdi.memory.is_busy():
        time.sleep(0.5)

    ftdi.memory.mem_action(file_path, False)
    ftdi.disable_cpu_reset()
    ftdi.spi.terminate()


if __name__ == "__main__":
    asyncio.run(main())
