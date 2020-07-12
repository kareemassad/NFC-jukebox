# Copied the code from the Read module
# Using this API and documentation https://spotipy.readthedocs.io/en/2.13.0/

import RPi.GPIO as GPIO
import spotipy
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
        id, text = reader.read()
        print(id)
        print(text)
        #take text stored and convert to suitable url
        #expect URI such as spotify:album:7n3QJc7TBOxXtlYh4Ssll8 (Adele album 21)
        spotifyURI = text
        devices()



finally:
        GPIO.cleanup()