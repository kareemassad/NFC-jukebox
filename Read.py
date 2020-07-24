# This code is used to read NFC tags using a Raspberry Pi 3B+

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import csv
from extractURI import getSpotifyURI

reader = SimpleMFRC522()

try:
        id, text = reader.read()
        print("Place your tag to be read!")
        #id represents the unique serial number of each tag
        getSpotifyURI(id)
        print(id)
        #text represents the text written to the tag
        print(text)
finally:
        GPIO.cleanup()