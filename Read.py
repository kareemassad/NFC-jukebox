# This code is used to read NFC tags using a Raspberry Pi 3B+

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import csv
from extractURI import getSpotifyURI

"""[summary]
Given an ID type integer, return the corresponding spotify URI
"""
def getSpotifyURI(ID):
        file = open('spotifyURICollection.csv', encoding='utf-8-sig')
        csv_file = csv.DictReader(file)
        for row in csv_file:
                #print(row['ID'])
                if(str(ID) == row['ID']):
                        URI = row['URI']
                        print(URI)
                        return URI
        #Base Case
        return "no match found"

reader = SimpleMFRC522()

try:
        print("Place your tag to be read!")
        id, text = reader.read()
        #id represents the unique serial number of each tag
        getSpotifyURI(id)
        print(id)
        #text represents the text written to the tag
        #print(text)
finally:
        GPIO.cleanup()