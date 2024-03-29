import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

# TODO add spotify cliendID, clientSecret, and redirectURI into env variables


def playSpotify(contextURI, deviceID):
    """This method takes a context URI and a Device ID then plays said URI on the given Device

    Args:
        contextURI (String): Contains the URI of the album/artist/playlist
        deviceID (String): Contains the device ID meant for playback
    """
    # "31876612233caf235184b622d80c84b51b39cc36"
    spotifyObject.start_playback(deviceID, contextURI, None)


def getAlbumTracks(albumURI):
    """This method takes an album URI and returns a list containing all of the URIs for the tracks in it. No longer required with the latest spotify update

    Args:
        albumURI (String): [A spotify album URI]

    Returns:
        tracks(list of strings): [Contains the album's tracks as spotify URI links]
    """
    i = 0
    n = 50
    result = spotifyObject.album_tracks(albumURI, n, 0, None)

    # append all track URIs into list tracks
    tracks = []
    for n in range(len(result['items'])):
        trackLinks = result['items'][n]['uri']
        tracks.append(trackLinks)
    return tracks


def findDeviceID():
    """ This method finds all devices available to play on a spotify account and returns the device to be used for playback. It always returns the ID of the Amazon Echo unless it is unavailable.

    Returns:
        deviceID(String): Returns the ID of the Amazon Echo if it is available.
        devices[0](String): If it isn't, returns the first other option.
    """
    # get all active devices
    result = spotifyObject.devices()
    #print(json.dumps(result, sort_keys=True, indent=4))

    # Store all device ID's found in a list
    devices = []
    for n in range(len(result['devices'])):
        deviceID = result['devices'][n]['id']
        devices.append(deviceID)

        # if spotify speaker exists, play on it. Otherwise, play on whatever.
        if(deviceID == "31876612233caf235184b622d80c84b51b39cc36"):
            return deviceID
    # Play on whatever is available first.
    # print(devices[0])
    return devices[0]


username = '22wtiqz6ow2wcjaoopq5k4vyy'
scope = 'user-read-private user-modify-playback-state user-read-playback-state'

# authentication
# remember to add cache to .gitignore
try:
    token = util.prompt_for_user_token(username, scope)
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

# create a spotify object
spotifyObject = spotipy.Spotify(auth=token)
# give album
albumURI = 'spotify:album:7n3QJc7TBOxXtlYh4Ssll8'
# get device to play on
deviceID = findDeviceID()
# play the album
playSpotify(albumURI, deviceID)
