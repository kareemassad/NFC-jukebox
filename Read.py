# This code is used to read NFC tags using a Raspberry Pi 3B+

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import csv
import os
import sys
import json
import spotipy
import time
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
from pushbullet.pushbullet import PushBullet
from device_selection import select_device_id
from catalog import find_album


def getSpotifyInfo(ID):
    """
    Given an id type integer, return the corresponding spotify uri

    Args:

        ID (Integer): A unique id given directly from each unique nfc tag.

    Returns:

        uri (String): A spotify uri pulled from a .csv file that directly coressponds to a specific id.
        artist (String): A spotify artist name pulled from a .csv file that directly coressponds to a specific id.
        album (String): A spotify album name pulled from a .csv file that directly coressponds to a specific id.
    """

    file = open("spotifyURICollection.csv", encoding="cp1252")
    csv_file = csv.DictReader(file)
    return find_album(csv_file, ID)


def playSpotify(contextURI, deviceID):
    """This method takes a context URI and a Device ID then plays said URI on the given Device

    Args:

        contextURI (String): Contains the URI of the album/artist/playlist
        deviceID (String): Contains the device ID meant for playback
    """
    # "31876612233caf235184b622d80c84b51b39cc36"
    spotifyObject.start_playback(deviceID, contextURI, None)
    print("It has played on this device: " + deviceID)


PREFERRED_DEVICE_ID = "31876612233caf235184b622d80c84b51b39cc36"


def findDeviceID():
    """Return the preferred or first available non-phone Spotify device."""
    result = spotifyObject.devices()
    available_devices = result.get("devices", [])
    return select_device_id(available_devices, PREFERRED_DEVICE_ID)


# exposing api key for now will get new and reset when done
client_id = "47b1df84dd804a17a77ddab564c05f79"
client_secret = "67681af49c0041959131bad5973529b6"
redirect_uri = "http://localhost:8888/callback"
pushbullet_api_key = YOUR_KEY_HERE

username = "22wtiqz6ow2wcjaoopq5k4vyy"
scope = "user-read-private user-modify-playback-state user-read-playback-state"

# PushBullet SMS module
pb = PushBullet(pushbullet_api_key)

# Get a list of devices
devices = pb.getDevices()
print(devices)


# authentication
# remember to add cache to .gitignore
try:
    token = util.prompt_for_user_token(
        username, scope, client_id, client_secret, redirect_uri
    )
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

# create a spotify object
spotifyObject = spotipy.Spotify(auth=token)
reader = SimpleMFRC522()

try:
    usedID = 000
    while True:
        print("Place your tag to be read !")
        # id represents the unique serial number of each tag
        id, text = reader.read()
        print(id)

        if usedID != id:
            # access data in URI variable
            albumInfo = getSpotifyInfo(id)
            if albumInfo is None:
                print("No album is configured for this NFC tag.")
                usedID = id
                time.sleep(2)
                continue

            print("That id represents this album: " + albumInfo[2])
            # get device to play on
            deviceID = findDeviceID()
            if deviceID is None:
                print("No non-phone Spotify device available. Retrying in 5 seconds.")
                time.sleep(5)
                continue
            # play the album
            playSpotify(albumInfo[0], deviceID)

            # Send a note
            note_title = "Played " + albumInfo[2]
            note_body = "Song played on " + deviceID
            pb.pushNote(devices[0]["iden"], note_title, note_body)

        usedID = id
        # slight time delay to handle requests better
        time.sleep(2)
finally:
    GPIO.cleanup()
