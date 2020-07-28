import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

#TODO add spotify cliendID, clientSecret, and redirectURI into env variables

def playTrack(trackURI):
    """This method start's playback on a 

    Args:
        trackURI (String): [Contains the URI of the album/artist/playlist]
    """
    spotifyObject.start_playback("31876612233caf235184b622d80c84b51b39cc36", trackURI ,None)

def getAlbumTracks(albumURI):
    """This method takes an album URI and returns a list containing all of the URIs for the tracks in it. No longer required with the latest spotify update

    Args:
        albumURI (String): [A spotify album URI]

    Returns:
        tracks(list of strings): [Contains the album's tracks as spotify URI links]
    """
    i = 0
    n = 50
    result = spotifyObject.album_tracks(albumURI, n, 0 ,None)

    #append all track URIs into list tracks
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
    #get all active devices
    result = spotifyObject.devices()
    print(json.dumps(result, sort_keys=True, indent=4))

    #Store all device ID's found in a list
    devices = []
    for n in range(len(result['devices'])):
        deviceID = result['devices'][n]['id']
        devices.append(deviceID)

        #if spotify speaker exists, play on it. Otherwise, play on whatever.
        if(deviceID == "31876612233caf235184b622d80c84b51b39cc36s"):
            return deviceID
    #Play on whatever is available first.
    print(devices[0])
    return devices[0]

username = '22wtiqz6ow2wcjaoopq5k4vyy'
scope = 'user-read-private user-modify-playback-state user-read-playback-state'

#authentication
try:
    token = util.prompt_for_user_token(username, scope)
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

#create a spotify object
spotifyObject = spotipy.Spotify(auth=token)


#get user information
user = spotifyObject.current_user()

#give album
albumURI = 'spotify:album:05J8PFXdYKeYNb8YjqqJYr'

findDeviceID()