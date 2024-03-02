"""import serial


ser = serial.Serial("/dev/ttyS0")

#ser.open()
while True:
	value = ser.read()
	print(value)
"""

# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example shows connecting to the PN532 with I2C (requires clock
stretching support), SPI, or UART. SPI is best, it uses the most pins but
is the most reliable and universally supported.
After initialization, try waving various 13.56MHz RFID cards over it!
"""

import board
import busio
from digitalio import DigitalInOut

#
# NOTE: pick the import that matches the interface being used
#
#from adafruit_pn532.i2c import PN532_I2C

# from adafruit_pn532.spi import PN532_SPI
from adafruit_pn532.uart import PN532_UART
"""
# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)

# Non-hardware
# pn532 = PN532_I2C(i2c, debug=False)

# With I2C, we recommend connecting RSTPD_N (reset) to a digital pin for manual
# harware reset
reset_pin = DigitalInOut(board.D6)
# On Raspberry Pi, you must also connect a pin to P32 "H_Request" for hardware
# wakeup! this means we don't need to do the I2C clock-stretch thing
req_pin = DigitalInOut(board.D12)
pn532 = PN532_I2C(i2c, debug=False, reset=reset_pin, req=req_pin)
"""
# SPI connection:
# spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
# cs_pin = DigitalInOut(board.D5)
# pn532 = PN532_SPI(spi, cs_pin, debug=False)

# UART connection
#uart = busio.UART(board.TX, board.RX, baudrate=115200, timeout=0.1)
import serial
uart = serial.Serial("/dev/ttyS0", baudrate = 115200, timeout = 0.1)
pn532 = PN532_UART(uart, debug=False)

ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

print("Waiting for RFID/NFC card...")
# while True:
#     # Check if a card is available to read
#     uid = pn532.read_passive_target(timeout=0.5)
#     print(".", end="")
#     # Try again if no card is available.
#     if uid is None:
#         continue
#     print("Found card with UID:", [hex(i) for i in uid])

while True:
    # Wait for a card to be available
    uid = pn532.read_passive_target()
    # Try again if no card found
    if uid is None:
        continue
    # Found a card, now try to read block 4 to detect the block type
    print('')
    print('Card UID 0x{0}'.format(binascii.hexlify(uid)))
    # Authenticate and read block 4
    if not pn532.mifare_classic_authenticate_block(uid, 4, PN532.MIFARE_CMD_AUTH_B,
                                                   CARD_KEY):
        print('Failed to authenticate with card!')
        continue
    data = pn532.mifare_classic_read_block(4)
    if data is None:
        print('Failed to read data from card!')
        continue
    # Check the header
    if data[0:2] !=  HEADER:
        print('Card is not written with proper block data!')
        continue
    # Parse out the block type and subtype
    print('User Id: {0}'.format(int(data[2:8].decode("utf-8"), 16)))