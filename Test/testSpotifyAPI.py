import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

#TODO add spotify cliendID, clientSecret, and redirectURI into env variables

def playTrack(trackURI):
    return spotifyObject.start_playback("31876612233caf235184b622d80c84b51b39cc36", None ,trackURI)

def getAlbumTracks(albumURI):
    #result is now a dict
    # track = spotifyObject.current_user_playing_track()
    # print(json.dumps(track, sort_keys=True, indent=4))
    # artist = track['item']['artists'][0]['name']
    # print(artist)
    # track = track['item']['name']
    # print(track)
    i = 0
    n = 50
    result = spotifyObject.album_tracks(albumURI, n, 0 ,None)

    #append all track URIs into list trackURIs
    trackURIs = []
    for n in range(len(result['items'])):
        trackLinks = result['items'][n]['uri']
        trackURIs.append(trackLinks)
    return trackURIs

#username from spotify main page
username = '22wtiqz6ow2wcjaoopq5k4vyy'
#changes based on what you want to do, read documentation
scope = 'user-read-private user-modify-playback-state user-read-playback-state'

#authentication
try:
    token = util.prompt_for_user_token(username, scope)
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

#create a spotify object
spotifyObject = spotipy.Spotify(auth=token)

#what device is playing
devices = spotifyObject.devices()
print(json.dumps(devices, sort_keys=True, indent=4))
deviceID = devices['devices'][1]['id']
print(deviceID)
#get user information
user = spotifyObject.current_user()
displayName = user['display_name']
follower = user['followers']['total']
#print(user, displayName, follower)

#Play a track
#trackURI = ['spotify:track:6SJLngO5LfdEldlJd1MWCs']
#playTrack(trackURI)

albumURI = 'spotify:album:37rNuexqEXWeSIOiJtn3A9'
albumtracks = getAlbumTracks(albumURI)
print(getAlbumTracks(albumURI))