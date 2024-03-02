// // #include <NfcAdapter.h>
// // #include <PN532/PN532/PN532.h>

// // #if 0 // use SPI
// //     #include <SPI.h>
// //     #include <PN532/PN532_SPI/PN532_SPI.h>
// //     PN532_SPI pn532spi(SPI, 9);
// //     NfcAdapter nfc = NfcAdapter(pn532spi);
// // #elif 0 // use hardware serial

// //     #include <PN532/PN532_HSU/PN532_HSU.h>
// //     PN532_HSU pn532hsu(Serial);
// //     NfcAdapter nfc(pn532hsu);
// // #elif 0  // use software serial

// //     #include <PN532/PN532_SWHSU/PN532_SWHSU.h>
// //     #include "SoftwareSerial.h"
// //     SoftwareSerial SWSerial(2, 3);
// //     PN532_SWHSU pn532swhsu(SWSerial);
// //     NfcAdapter nfc(pn532swhsu);
// // #else //use I2C

// //     #include <Wire.h>
// //     #include <PN532/PN532_I2C/PN532_I2C.h>

// //     PN532_I2C pn532_i2c(Wire);
// //     NfcAdapter nfc = NfcAdapter(pn532_i2c);
// // #endif

// // void setup(void) {
// //     Serial.begin(9600);
// //     Serial.println("NDEF Reader");
// // }

// // void loop(void) {
// //     Serial.println("\nScan a NFC tag\n");
// //     if (nfc.tagPresent()) {
// //         Serial.println("present");
// //         NfcTag tag = nfc.read();
// //         tag.print();
// //     }
// //     delay(500);
// // }


// #include <Wire.h>
// #include <NfcAdapter.h>
// // #include <PN532_I2C.h>
// #include <PN532/PN532/PN532.h>
// #include <PN532/PN532_I2C/PN532_I2C.h>
// // #include <PN532.h>
// #include <NfcAdapter.h>

// PN532_I2C pn532_i2c(Wire);
// NfcAdapter nfc = NfcAdapter(pn532_i2c);


// void setup(void) {
//     Serial.begin(9600);
//     Serial.println("NDEF Reader");
//     nfc.begin();
// }

// void loop(void) {
//     Serial.println("\nScan a NFC tag\n");
//     if (nfc.tagPresent())
//     {
//         NfcTag tag = nfc.read();
//         tag.print();
//     }
//     delay(500);
// }

// for Hardware Serial
/*#include <PN532_HSU.h>
  #include <PN532.h>
  PN532_HSU pn532hsu( Serial );
  PN532 nfc( pn532hsu );
*/

// for Software Serial
#include <NfcAdapter.h>
#include <PN532/PN532/PN532.h>
#include <SoftwareSerial.h>
#include <PN532/PN532_SWHSU/PN532_SWHSU.h>
//#include <PN532_SWHSU.h>
//#include <PN532.h>
SoftwareSerial SWSerial( 2, 3 ); // RX, TX
PN532_SWHSU pn532swhsu( SWSerial );
PN532 nfc( pn532swhsu );


String tagId = "None", dispTag = "None";
byte nuidPICC[4];

void setup(void) {

  Serial.begin(115200);
  Serial.println("Hello Maker!");
  //  Serial2.begin(115200, SERIAL_8N1, RXD2, TXD2);

  nfc.begin();

  uint32_t versiondata = nfc.getFirmwareVersion();
  if (! versiondata) {
    Serial.print("Didn't Find PN53x Module");
    while (1); // Halt
  }

  // Got valid data, print it out!
  Serial.print("Found chip PN5"); Serial.println((versiondata >> 24) & 0xFF, HEX);
  Serial.print("Firmware ver. "); Serial.print((versiondata >> 16) & 0xFF, DEC);
  Serial.print('.'); Serial.println((versiondata >> 8) & 0xFF, DEC);

  // Configure board to read RFID tags
  nfc.SAMConfig();

  Serial.println("Waiting for an ISO14443A Card ...");

}

void loop() {
  readNFC();
}

void readNFC() {

  boolean success;
  uint8_t uid[] = { 0, 0, 0, 0, 0, 0, 0 };  // Buffer to store the returned UID
  uint8_t uidLength;                       // Length of the UID (4 or 7 bytes depending on ISO14443A card type)
  success = nfc.readPassiveTargetID(PN532_MIFARE_ISO14443A, &uid[0], &uidLength);

  if (success) {
    Serial.print("UID Length: "); Serial.print(uidLength, DEC); Serial.println(" bytes");
    Serial.print("UID Value: ");

    for (uint8_t i = 0; i < uidLength; i++) {
      nuidPICC[i] = uid[i];
      Serial.print(" "); Serial.print(uid[i], DEC);
    }
    Serial.println();
    tagId = tagToString(nuidPICC);
    dispTag = tagId;
    Serial.print(F("tagId is : "));
    Serial.println(tagId);
    Serial.println("");

    delay(1000);  // 1 second halt

  } else {
    // PN532 probably timed out waiting for a card
    //Serial.println("Timed out! Waiting for a card...");
  }
}

String tagToString(byte id[4]) {
  String tagId = "";
  for (byte i = 0; i < 4; i++) {
    if (i < 3) tagId += String(id[i]) + ".";
    else tagId += String(id[i]);
  }
  return tagId;
}
