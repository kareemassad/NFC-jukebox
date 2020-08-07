# This code is used to read NFC tags using a Raspberry Pi 3B+

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import csv
import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError
from pushbullet.pushbullet import PushBullet


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
    for row in csv_file:
        # print(row['ID'])
        # DONE: concantinate ID to a string
        if str(ID) == row["ID"]:
            uri = row["URI"]
            artist = row["Artist"]
            album = row["Album"]
            print(uri)
            return uri, artist, album
    # Base Case
    return "no match found"


def playSpotify(contextURI, deviceID):
    """This method takes a context URI and a Device ID then plays said URI on the given Device

    Args:

        contextURI (String): Contains the URI of the album/artist/playlist
        deviceID (String): Contains the device ID meant for playback
    """
    # "31876612233caf235184b622d80c84b51b39cc36"
    spotifyObject.start_playback(deviceID, contextURI, None)
    print("It has played on this device: " + deviceID)


def findDeviceID():
    """ This method finds all devices available to play on a spotify account and returns the device to be used for playback. It always returns the ID of the Amazon Echo unless it is unavailable.

    Returns:

        deviceID(String): Returns the id of the Amazon Echo if it is available or the next available device
    """
    # get all active devices
    result = spotifyObject.devices()
    # print(json.dumps(result, sort_keys=True, indent=4))

    # Store all device ID's found in a list
    devices = []
    for n in range(len(result["devices"])):
        deviceID = result["devices"][n]["id"]
        devices.append(deviceID)

        # if spotify speaker exists, play on it. Otherwise, play on whatever.
        if deviceID == "31876612233caf235184b622d80c84b51b39cc36":
            return deviceID
    # Play on whatever is available first.
    # print(devices[0])
    return devices[0]


# exposing api key for now will get new and reset when done
client_id = '47b1df84dd804a17a77ddab564c05f79'
client_secret = '67681af49c0041959131bad5973529b6'
redirect_uri = 'http://localhost:8888/callback'
api_key = YOUR_KEY_HERE

username = "22wtiqz6ow2wcjaoopq5k4vyy"
scope = "user-read-private user-modify-playback-state user-read-playback-state"

# PushBullet SMS module
pb = PushBullet(api_key)

# Get a list of devices
devices = pb.getDevices()
print(devices)


# authentication
# remember to add cache to .gitignore
try:
    token = util.prompt_for_user_token(
        username, scope, client_id, client_secret, redirect_uri)
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

# create a spotify object
spotifyObject = spotipy.Spotify(auth=token)
reader = SimpleMFRC522()

try:
    usedID = 000
    while(True):
        print("Place your tag to be read !")
        # id represents the unique serial number of each tag
        id, text = reader.read()
        print(id)

        if(usedID != id):
            # access data in URI variable
            albumInfo = getSpotifyInfo(id)
            print("That id represents this album: " + albumInfo.album)
            if albumURI == "no match found":
                sys.exit()
            # get device to play on
            deviceID = findDeviceID()
            # play the album
            playSpotify(albumInfo.uri, deviceID)

            # Send a note
            note_title = 'Played ' + albumInfo.title
            note_body = 'Song played on ' + deviceID
            pb.pushNote(devices[0]["iden"], note_title, note_body)

        usedID = id
finally:
    GPIO.cleanup()
