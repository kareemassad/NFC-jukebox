import os
import sys
import json
import spotipy
import webbrowser
import spotipy.util as util
from json.decoder import JSONDecodeError

def playURI(uri):
    return spotifyObject.start_playback("31876612233caf235184b622d80c84b51b39cc36", None ,uri)


#TODO add spotify cliendID, clientSecret, and redirectURI into env variables

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
#deviceID = devices['devices'][0]['id']

#get user information
user = spotifyObject.current_user()
displayName = user['display_name']
follower = user['followers']['total']
#print(user, displayName, follower)

uriToPlay = ['spotify:track:6SJLngO5LfdEldlJd1MWCs']

print(playURI(uriToPlay))

# while True:

#     print()
#     print(">>> Welcome to Spotify " + displayName + " :)")
#     print(">>> You have " + str(follower) + " followers.")
#     print()
#     print("0 - Search for an artist")
#     print("1 - exit")
#     print()
#     choice = input("Enter your choice: ")