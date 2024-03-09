import time
import binascii

from pn532pi import Pn532, pn532
from pn532pi import Pn532Hsu

# Set the desired interface to True
HSU = True

PN532_HSU = Pn532Hsu(Pn532Hsu.RPI_MINI_UART)
nfc = Pn532(PN532_HSU)

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
            #  We probably have a Mifare Classic card ...
            print("Seems to be a Mifare Classic card (4 byte UID)")

            #  Now we need to try to authenticate it for read/write access
            #  Try with the factory default KeyA: 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF
            print("Trying to authenticate block 4 with default KEYA value")
            keya = bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

            #  Start with block 4 (the first block of sector 1) since sector 0
            #  contains the manufacturer data and it's probably better just
            #  to leave it alone unless you know what you're doing
            for i in range(0, 32):
                success = nfc.mifareclassic_AuthenticateBlock(uid, i, 0, keya)

                if (success):

                    #  Try to read the contents of block 4
                    success, data = nfc.mifareclassic_ReadDataBlock(i)

                    if (success):
                        #  Data seems to have been read ... spit it out
                        print(f"{i}:{data}")
                        i+=1

                    else:
                        print("FAIL")
                        i+=1
                else:
                    print("FAIL")
                    i +=1

        elif (len(uid) == 7):
            #  We probably have a Mifare Ultralight card ...
            print("Seems to be a Mifare Ultralight tag (7 byte UID)")

            #  Try to read the first general-purpose user page (#4)
            print("Reading page 4")
            for i in range(0, 32):
                success, data = nfc.mifareultralight_ReadPage(i)
                if (success):
                    #  Data seems to have been read ... spit it out
                    print(f"{i}:{data}")
                    i+=1
                else:
                    print("FAIL")
                    i+=1

    return False

if __name__ == '__main__':
    setup()
    found = loop()
    while not found:
        time.sleep(5)
        found = loop()