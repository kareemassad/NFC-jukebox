# This code is used to read NFC tags using a Raspberry Pi 3B+

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import csv
from extractURI import getSpotifyURI

#

def getSpotifyURI(ID):
        """
        Given an ID type integer, return the corresponding spotify URI

        Args:
            ID ([Integer]): [A unique ID given directly from each unique NFC tag]

        Returns:
            URI ([String]): [A spotify URI pulled from a .csv file that directly coressponds a specific ID]
        """
        
        file = open('spotifyURICollection.csv', encoding='utf-8-sig')
        csv_file = csv.DictReader(file)
        for row in csv_file:
                #print(row['ID'])
                #DONE: concantinate ID to a string 
                if(str(ID) == row['ID']):
                        URI = row['URI']
                        print(URI)
                        return URI
        #Base Case
        return "no match found"

def playSpotify(URI):

        return 

reader = SimpleMFRC522()

try:
        print("Place your tag to be read!")
        id, text = reader.read()
        #id represents the unique serial number of each tag
        #access data in URI variable
        getSpotifyURI(id)
        #pass URI variable in new function that interfaces with spotify
        #TODO: Create a new function that plays a song on spotify based on the URI 


        print(id)
        #text represents the text written to the tag
        #print(text)
finally:
        GPIO.cleanup()