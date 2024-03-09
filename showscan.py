import digitalio, time, binascii, board, cv2, neopixel
from PIL import Image, ImageDraw
from adafruit_rgb_display import st7735
from pn532pi import Pn532, pn532
from pn532pi import Pn532Hsu

def setup():
    nfc.begin()

    versiondata = nfc.getFirmwareVersion()
    if (not versiondata):
        print("Didn't find PN53x board")
        raise RuntimeError("Didn't find PN53x board")  # halt

    #  Got ok data, print it out!
    print("Found chip PN5 {:#x} Firmware ver. {:d}.{:d}".format((versiondata >> 24) & 0xFF, (versiondata >> 16) & 0xFF,
                                                                (versiondata >> 8) & 0xFF))

    #  configure board to read RFID tags
    nfc.SAMConfig()

    print("Waiting for an ISO14443A Card ...")


def loop():
    #  Wait for an ISO14443A type cards (Mifare, etc.).  When one is found
    #  'uid' will be populated with the UID, and uidLength will indicate
    #  if the uid is 4 bytes (Mifare Classic) or 7 bytes (Mifare Ultralight)
    print('Check Scan')
    check_uid = True
    while check_uid:
        success, uid = nfc.readPassiveTargetID(pn532.PN532_MIFARE_ISO14443A_106KBPS)
        if(success):
            check_uid = False

    if (success):
        #  Display some basic information about the card
        print("Found an ISO14443A card")
        print("UID Length: {:d}".format(len(uid)))
        print("UID Value: {}".format(binascii.hexlify(uid)))

        if (len(uid) == 4):
            print("FAIL : Wrong Card")
            return False

        elif (len(uid) == 7):
            #  We probably have a Mifare Ultralight card ...
            print("Seems to be a Mifare Ultralight tag (7 byte UID)")

            #  Try to read the first general-purpose user page (#4)
            print("Reading page 4")
            success, data = nfc.mifareultralight_ReadPage(4)
            value = 6
            if (success):
                lenght = data[1]
                print(f"data lenght: {lenght}")
                value = ((lenght + 3) // 4 + 5)
                print(value)
            else:
                return False
            response = ""
            for i in range(6, value):
                success, data = nfc.mifareultralight_ReadPage(i)
                if (success):
                    #  Data seems to have been read ... spit it out
                    response += data.decode("utf-8", errors='ignore')
                    print(f"{i}:{data}")
                    i+=1
                else:
                    print("FAIL")
                    return False
        return response

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

ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(board.D21, 14, brightness=0.2, auto_write=False, pixel_order=ORDER)

pixels.fill((0,0,255))
pixels.show()

# Setup SPI bus using hardware SPI:
spi = board.SPI()

disp = st7735.ST7735R(spi, rotation=90,
    dc=digitalio.DigitalInOut(board.D25),
    cs=digitalio.DigitalInOut(board.CE0),
    rst=digitalio.DigitalInOut(board.D24),
    baudrate=24000000,
)

HSU = True

PN532_HSU = Pn532Hsu(Pn532Hsu.RPI_MINI_UART)
nfc = Pn532(PN532_HSU)

# Create blank image for drawing.
disp.image(draw_black_box(disp))
# Display image.
path = "scanhere.jpg"
disp.image(display_new_image(path, disp))

setup()
response = loop()

pixels.fill((0,255,0))
pixels.show()

if not response:
    print("ERROR")
    # Display image.
    path = "error.jpg"
    disp.image(display_new_image(path, disp))
else :
    path = "blinka.jpg"
    image = cv2.imread(path)
    text = response[1:]
    font = cv2.FONT_HERSHEY_SIMPLEX 
    org = (200, 450)
    fontScale = 2
    color = (0, 0, 255)
    thickness = 6
    imagenamed = cv2.putText(image, text, org, font, fontScale, color, thickness, cv2.LINE_AA, False)
    newpath = "test.jpg"
    cv2.imwrite(newpath, imagenamed)

    disp.image(display_new_image(newpath, disp))
    
while True:
    pixels.fill((0,0,0))
    for i in range(14):
        pixels[i] = (255, 0, 0)
        pixels.show()
        time.sleep(.25)