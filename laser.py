import RPi.GPIO as GPIO
import time

# Use "GPIO" pin numbering
GPIO.setmode(GPIO.BCM)

# Set LED pin as output
GPIO.setup(16, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

not_good =True
while not_good:
    
    state_magnet1 = GPIO.input(16)
    if state_magnet1:
        print("GOOD JOB")
    else:
        print("LOSER")
    
    time.sleep(0.1)
