import RPi.GPIO as GPIO
import time
import serial
from adafruit_pn532.uart import PN532_UART

uart = serial.Serial("/dev/ttyS0", baudrate = 115200, timeout = 0.1)
pn532 = PN532_UART(uart, debug=False)

not_good = False
found_device = True

ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()

print("Waiting for RFID/NFC card...")
while found_device:
    # Check if a card is available to read
    uid = pn532.read_passive_target(timeout=0.5)
    # print(".", end="")
    # Try again if no card is available.
    if uid is None:
        continue
    else :
        print("Found card with UID:", [hex(i) for i in uid])
        not_good = True
        found_device = False

magnet1 = 12 #32
magnet2 = 1  #28
magnet3 = 7  #26
magnet4 = 8  #26
magnet5 = 25 #22
magnet6 = 24 #18
magnet7 = 23 #16

# Use "GPIO" pin numbering
GPIO.setmode(GPIO.BCM)

# Set LED pin as output
GPIO.setup(magnet1, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(magnet2, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(magnet3, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(magnet4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(magnet5, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(magnet6, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(magnet7, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

not_good = True

while not_good:
    
    state_magnet1 = GPIO.input(magnet1)
    state_magnet2 = GPIO.input(magnet2)
    state_magnet3 = GPIO.input(magnet3)
    state_magnet4 = GPIO.input(magnet4)
    state_magnet5 = GPIO.input(magnet5)
    state_magnet6 = GPIO.input(magnet6)
    state_magnet7 = GPIO.input(magnet7)

    if (state_magnet1 and state_magnet2 and state_magnet3 and state_magnet4 and state_magnet5 and state_magnet6 and state_magnet7):
        print("CONGRATS")
        not_good = False
    time.sleep(0.5)
