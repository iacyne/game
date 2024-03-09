import digitalio, time, binascii, board
import board
from PIL import Image, ImageDraw
from adafruit_rgb_display import st7735
from pn532pi import Pn532, pn532
from pn532pi import Pn532Hsu

def draw_black_box(disp):
    height = disp.width
    width = disp.height
    rgbimage = Image.new("RGB", (width, height))
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(rgbimage)
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    return rgbimage

def display_new_image(path, disp):
    height = disp.width
    width = disp.height
    folderimage = Image.open(path)
    # Scale the image to the smaller screen dimension
    image_ratio = folderimage.width / folderimage.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = folderimage.width * height // folderimage.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = folderimage.height * width // folderimage.width
    imageresized = folderimage.resize((scaled_width, scaled_height), Image.BICUBIC)

    # Crop and center the image
    x = scaled_width // 2 - width // 2
    y = scaled_height // 2 - height // 2
    imageresized = imageresized.crop((x, y, x + width, y + height))
    return imageresized

# Setup SPI bus using hardware SPI:
spi = board.SPI()

disp = st7735.ST7735R(spi, rotation=90,
    dc=digitalio.DigitalInOut(board.D25),
    cs=digitalio.DigitalInOut(board.CE0),
    rst=digitalio.DigitalInOut(board.D24),
    baudrate=24000000,
)

# Create blank image for drawing.
disp.image(draw_black_box(disp))
# Display image.
path = "scanhere.jpg"
disp.image(display_new_image(path, disp))


# import time
# import binascii

# from pn532pi import Pn532, pn532
# from pn532pi import Pn532Hsu

# # Set the desired interface to True
# HSU = True

# PN532_HSU = Pn532Hsu(Pn532Hsu.RPI_MINI_UART)
# nfc = Pn532(PN532_HSU)

# def setup():
#     nfc.begin()

#     versiondata = nfc.getFirmwareVersion()
#     if (not versiondata):
#         print("Didn't find PN53x board")
#         raise RuntimeError("Didn't find PN53x board")  # halt

#     #  Got ok data, print it out!
#     print("Found chip PN5 {:#x} Firmware ver. {:d}.{:d}".format((versiondata >> 24) & 0xFF, (versiondata >> 16) & 0xFF,
#                                                                 (versiondata >> 8) & 0xFF))

#     #  configure board to read RFID tags
#     nfc.SAMConfig()

#     print("Waiting for an ISO14443A Card ...")


# def loop():
#     #  Wait for an ISO14443A type cards (Mifare, etc.).  When one is found
#     #  'uid' will be populated with the UID, and uidLength will indicate
#     #  if the uid is 4 bytes (Mifare Classic) or 7 bytes (Mifare Ultralight)
#     print('Check Scan')
#     check_uid = True
#     while check_uid:
#         success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)
#         if(success):
#             check_uid = False

#     if (success):
#         #  Display some basic information about the card
#         print("Found an ISO14443A card")
#         print("UID Length: {:d}".format(len(uid)))
#         print("UID Value: {}".format(binascii.hexlify(uid)))

#         if (len(uid) == 4):
#             print("FAIL : Wrong Card")
#             return False
#             # #  We probably have a Mifare Classic card ...
#             # print("Seems to be a Mifare Classic card (4 byte UID)")

#             # #  Now we need to try to authenticate it for read/write access
#             # #  Try with the factory default KeyA: 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF
#             # print("Trying to authenticate block 4 with default KEYA value")
#             # keya = bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

#             # #  Start with block 4 (the first block of sector 1) since sector 0
#             # #  contains the manufacturer data and it's probably better just
#             # #  to leave it alone unless you know what you're doing
#             # for i in range(0, 32):
#             #     success = nfc.mifareclassic_AuthenticateBlock(uid, i, 0, keya)

#             #     if (success):

#             #         #  Try to read the contents of block 4
#             #         success, data = nfc.mifareclassic_ReadDataBlock(i)

#             #         if (success):
#             #             #  Data seems to have been read ... spit it out
#             #             print(f"{i}:{data}")
#             #             i+=1

#             #         else:
#             #             print("FAIL")
#             #             i+=1
#             #     else:
#             #         print("FAIL")
#             #         i +=1

#         elif (len(uid) == 7):
#             #  We probably have a Mifare Ultralight card ...
#             print("Seems to be a Mifare Ultralight tag (7 byte UID)")

#             #  Try to read the first general-purpose user page (#4)
#             print("Reading page 4")
#             success, data = nfc.mifareultralight_ReadPage(4)
#             value = 6
#             if (success):
#                 lenght = data[1]
#                 print(f"data lenght: {lenght}")
#                 value = ((lenght + 3) // 4 + 5)
#                 print(value)
#             else:
#                 return False
#             response = ""
#             for i in range(6, value):
#                 success, data = nfc.mifareultralight_ReadPage(i)
#                 if (success):
#                     #  Data seems to have been read ... spit it out
#                     response += data.decode("utf-8", errors='ignore')
#                     print(f"{i}:{data}")
#                     i+=1
#                 else:
#                     print("FAIL")
#                     return False
#             print(response)

#     return False

# if __name__ == '__main__':
#     setup()
#     found = loop()
#     while not found:
#         time.sleep(5)
#         found = loop()