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


def getSpotifyURI(ID):
    """
    Given an ID type integer, return the corresponding spotify URI

    Args:
        ID ([Integer]): [A unique ID given directly from each unique NFC tag]

    Returns:
        URI ([String]): [A spotify URI pulled from a .csv file that directly coressponds a specific ID]
    """

    file = open("spotifyURICollection.csv", encoding="utf-8-sig")
    csv_file = csv.DictReader(file)
    for row in csv_file:
        # print(row['ID'])
        # DONE: concantinate ID to a string
        if str(ID) == row["ID"]:
            URI = row["URI"]
            print(URI)
            return URI
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
        deviceID(String): Returns the ID of the Amazon Echo if it is available.
        devices[0](String): If it isn't, returns the first other option.
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


client_id = '47b1df84dd804a17a77ddab564c05f79'
client_secret = '67681af49c0041959131bad5973529b6'
redirect_uri = 'http://localhost:8888/callback'

username = "22wtiqz6ow2wcjaoopq5k4vyy"
scope = "user-read-private user-modify-playback-state user-read-playback-state"

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
    while(True):
        print("Place your tag to be read !")
        # id represents the unique serial number of each tag
        id, text = reader.read()
        print(id)

        # access data in URI variable
        albumURI = getSpotifyURI(id)
        print("That id represents this album: " + albumURI)
        if albumURI == "no match found":
            sys.exit()
        # get device to play on
        deviceID = findDeviceID()
        # play the album
        playSpotify(albumURI, deviceID)
finally:
    GPIO.cleanup()
