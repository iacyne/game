import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

#reader.write("ARNAUD LA PUTE")

time.sleep(2)

while True:
	id, text = reader.read()
	print(id)
	print(text)
